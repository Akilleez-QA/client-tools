#ifndef STARTUP_BRIDGE23_BACKEND_H
#define STARTUP_BRIDGE23_BACKEND_H
#include "../host-candidate/registry_resolver.h"
#include "../session-version22/session_version_host.h"
#include "reply.h"
#include <Mss.h>
// Same single Backend owner as the exercised live candidate, narrowed to this
// startup/metadata/driver slice. No SessionLifecycle or fixture expectations.
struct Backend {
    MilesTransport::ResourceRegistry registry;
    MilesHost::RegistryResolver resolver;
    MilesStartup::SessionInputs metadataInputs;
    HMODULE module;
    HDIGDRIVER driver;
    MilesWire::Handle driverId;
    bool started, shutdown;
    unsigned metadataInvocations;
    explicit Backend(const char *expectedPath)
        : resolver(registry), module(0), driver(0), started(false), shutdown(false),
          metadataInvocations(0) {
        driverId = MilesWire::Handle();
        require(GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,
                                   reinterpret_cast<LPCSTR>(&::AIL_startup), &module) != 0,
                "hold actual imported vendor module");
        char loaded[MAX_PATH] = {};
        DWORD n = GetModuleFileNameA(module, loaded, MAX_PATH);
        if (!n || n >= MAX_PATH || _stricmp(loaded, expectedPath)) {
            FreeLibrary(module);
            module = 0;
            throw std::runtime_error("imported module path mismatch");
        }
        printf("loaded_dll=%s\n", loaded);
    }
    ~Backend() {
        if (started) {
            ::AIL_shutdown();
            puts("FAIL emergency vendor cleanup");
        }
        if (module)
            FreeLibrary(module);
    }
    StartupBridge::OwnedReply execute(const MilesWire::Header &h, const MilesWire::Call &c,
                                      const std::vector<unsigned char> &frame) {
        using namespace StartupBridge;
        OwnedReply out;
        out.result.transport_status = InvalidFields;
        // Narrow native25 non-callback slice; reuse reviewed SDK dispatcher.
        switch (h.opcode) {
        case MilesWire::AIL_start_sample:
        case MilesWire::AIL_stop_sample:
        case MilesWire::AIL_sample_status:
        case MilesWire::AIL_set_sample_loop_count:
        case MilesWire::AIL_set_sample_loop_block:
        case MilesWire::AIL_set_sample_ms_position:
        case MilesWire::AIL_set_sample_position:
        case MilesWire::AIL_sample_position:
        case MilesWire::AIL_set_sample_playback_rate:
        case MilesWire::AIL_sample_playback_rate:
        case MilesWire::AIL_set_sample_volume_levels:
        case MilesWire::AIL_sample_volume_levels:
        case MilesWire::AIL_set_sample_reverb_levels:
        case MilesWire::AIL_sample_reverb_levels:
        case MilesWire::AIL_set_sample_3D_position:
        case MilesWire::AIL_set_sample_3D_velocity_vector:
        case MilesWire::AIL_set_sample_3D_distances:
        case MilesWire::AIL_set_sample_occlusion:
        case MilesWire::AIL_set_sample_obstruction:
            if (c.target.kind != MilesWire::OwnedSample) {
                out.result.transport_status = InvalidResource;
                return out;
            }
            // fall through to the shared lifecycle and real SDK dispatcher
        case MilesWire::AIL_sample_ms_position:
        case MilesWire::AIL_end_sample:
        case MilesWire::AIL_set_listener_3D_position:
        case MilesWire::AIL_set_listener_3D_velocity_vector:
        case MilesWire::AIL_set_listener_3D_orientation:
        case MilesWire::AIL_set_3D_rolloff_factor:
        case MilesWire::AIL_serve:
        case MilesWire::AIL_room_type:
        case MilesWire::AIL_set_room_type:
            if (!started || shutdown) {
                out.result.transport_status = LifecycleRefused;
                return out;
            }
            switch (MilesHost::dispatch(h.opcode, c, out.result, resolver)) {
            case MilesHost::Complete: out.result.transport_status = Success; break;
            case MilesHost::Unsupported: out.result.transport_status = Unsupported; break;
            case MilesHost::InvalidResource: out.result.transport_status = InvalidResource; break;
            case MilesHost::InvalidFields: out.result.transport_status = InvalidFields; break;
            }
            return out;
        default:
            break;
        }
        if (h.opcode == MilesWire::AIL_allocate_sample_handle ||
            h.opcode == MilesWire::AIL_release_sample_handle) {
            if (c.callback || c.reserved || c.output_mask || c.bytes.offset || c.bytes.length ||
                c.text.offset || c.text.length || !nullHandle(c.resource)) return out;
            for (unsigned i = 0; i < 8; ++i) if (c.value[i]) return out;
            if (!started || shutdown) {
                out.result.transport_status = LifecycleRefused;
                return out;
            }
            void *local = 0;
            const bool allocating = h.opcode == MilesWire::AIL_allocate_sample_handle;
            if (!registry.resolve(c.target, allocating ? MilesWire::Driver : MilesWire::OwnedSample,
                                  local)) {
                out.result.transport_status = InvalidResource;
                return out;
            }
            if (allocating) {
                MilesTransport::ResourceRegistry::Reservation reservation;
                require(registry.reserve(MilesWire::OwnedSample, c.target, reservation),
                        "sample tracking capacity before vendor allocation");
                PendingSample pending; // constructed before vendor work; cannot allocate
                pending.sample = ::AIL_allocate_sample_handle(static_cast<HDIGDRIVER>(local));
                if (pending.sample) {
                    require(registry.publish(reservation, pending.sample, out.result.resource),
                            "publish reserved sample identity");
                    pending.sample = 0; // registry now owns shutdown/release tracking
                }
                // Null allocation cancels its unpublished reservation on scope exit.
            } else {
                ::AIL_release_sample_handle(static_cast<HSAMPLE>(local));
                require(registry.retire(c.target), "retire sample after confirmed release");
            }
            out.result.transport_status = Success;
            return out;
        }
        if (metadata(h.opcode)) {
            const MilesStartup::Status shape = MilesStartup::validate(h.opcode, c, bytes(frame));
            if (shape != MilesStartup::Complete) {
                out.result.transport_status = mapMetadata(shape);
                return out;
            }
            if (shutdown || (!started && h.opcode != MilesWire::AIL_set_redist_directory)) {
                out.result.transport_status = LifecycleRefused;
                return out;
            }
            MilesStartup::Reply local;
            ++metadataInvocations;
            const MilesStartup::Status status =
                MilesStartup::dispatch(h.opcode, c, bytes(frame), local, resolver, metadataInputs);
            out.result = local.result;
            out.result.transport_status = mapMetadata(status);
            out.text.swap(local.text);
            return out;
        }
        if (h.opcode == MilesWire::SessionVersion) {
            MilesWire::Header checked = {};
            if (!MilesSessionVersion::validateQuery(bytes(frame), checked))
                return out;
            if (shutdown) {
                out.result.transport_status = LifecycleRefused;
                return out;
            }
            std::vector<unsigned char> encoded;
            if (!MilesSessionVersion::queryCurrentDll(bytes(frame), module, encoded)) {
                out.result.transport_status = VersionQueryFailed;
                return out;
            }
            require(decodeReply(bytes(encoded), h, out), "owned version adapter result");
            return out;
        }
        if (c.callback || c.reserved || c.output_mask || c.bytes.length || c.text.length ||
            !nullHandle(c.target) || !nullHandle(c.resource))
            return out;
        unsigned values = 0;
        switch (h.opcode) {
        case MilesWire::AIL_open_digital_driver:
            values = 4;
            break;
        case MilesWire::AIL_startup:
        case MilesWire::AIL_shutdown:
        case MilesWire::SessionClose:
            break;
        default:
            out.result.transport_status = Unsupported;
            return out;
        }
        for (unsigned i = values; i < 8; ++i)
            if (c.value[i])
                return out;
        out.result.transport_status = LifecycleRefused;
        if (h.opcode == MilesWire::AIL_startup) {
            if (started || shutdown)
                return out;
            const S32 value = ::AIL_startup();
            started = value != 0;
            out.result.return_bits = static_cast<uint32_t>(value);
            out.result.transport_status = Success;
            printf("vendor startup=%ld\n", value);
            return out;
        }
        if (h.opcode == MilesWire::SessionClose) {
            if (!started && shutdown && !driver)
                out.result.transport_status = Success;
            return out;
        }
        if (!started || shutdown)
            return out;
        if (h.opcode == MilesWire::AIL_open_digital_driver) {
            if (driver || c.value[0] != 22050 || c.value[1] != 16 || c.value[2] != 2 || c.value[3])
                return out;
            MilesTransport::ResourceRegistry::Reservation reservation;
            require(registry.reserve(MilesWire::Driver, MilesWire::Handle(), reservation),
                    "driver tracking capacity before vendor open");
            driver = ::AIL_open_digital_driver(22050, 16, MSS_MC_STEREO, 0);
            if (driver)
                require(registry.publish(reservation, driver, driverId),
                        "publish reserved driver identity");
            out.result.resource = driverId;
            out.result.transport_status = Success;
            return out;
        }
        if (h.opcode == MilesWire::AIL_shutdown) {
            ::AIL_shutdown();
            started = false;
            shutdown = true;
            if (driver) {
                require(registry.retire(driverId), "retire driver after shutdown");
                driver = 0;
            }
            printf("vendor shutdown complete; retained directory bytes=%u\n",
                   static_cast<unsigned>(metadataInputs.retainedBytes()));
            out.result.transport_status = Success;
            return out;
        }
        return out;
    }

  private:
    struct PendingSample {
        HSAMPLE sample;
        PendingSample() : sample(0) {}
        ~PendingSample() { if (sample) ::AIL_release_sample_handle(sample); }
      private:
        PendingSample(const PendingSample &);
        PendingSample &operator=(const PendingSample &);
    };
    Backend(const Backend &);
    Backend &operator=(const Backend &);
};
#endif
