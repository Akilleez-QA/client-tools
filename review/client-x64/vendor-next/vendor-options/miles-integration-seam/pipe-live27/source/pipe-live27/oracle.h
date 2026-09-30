#ifndef PIPE_LIVE27_ORACLE_H
#define PIPE_LIVE27_ORACLE_H
// Only original SDK getters. All setters under test go through Backend::execute.
static_assert(ENVIRONMENT_ROOM == 2, "precommitted ROOM value");
static_assert(ENVIRONMENT_GENERIC == 0, "precommitted GENERIC value");
static_assert(MSS_MC_STEREO == 2, "precommitted stereo value");
struct Oracle27 {
    Backend &backend;
    S32 originalRoom;
    bool savedRoom;
    explicit Oracle27(Backend &owner) : backend(owner), originalRoom(0), savedRoom(false) {}
    static uint32_t bits(F32 value) {
        static_assert(sizeof(F32) == sizeof(uint32_t), "F32 bit extent");
        uint32_t result = 0;
        std::memcpy(&result, &value, sizeof result);
        return result;
    }
    static void check(unsigned request, const char *field, F32 actual, F32 expected) {
        printf("state request=%u field=%s actual=%08x expected=%08x\n", request, field,
               bits(actual), bits(expected));
        require(bits(actual) == bits(expected), "fixed original-DLL float readback");
    }
    void position(unsigned request) {
        F32 x = 0, y = 0, z = 0;
        ::AIL_listener_3D_position(backend.driver, &x, &y, &z);
        check(request, "position.x", x, -1.25f);
        check(request, "position.y", y, 2.5f);
        check(request, "position.z", z, -3.75f);
    }
    void room(unsigned request, const StartupBridge::OwnedReply &reply, S32 expected,
              bool facadeQuery) {
        const S32 actual = ::AIL_room_type(backend.driver);
        printf("room request=%u actual=%d expected=%d\n", request, actual, expected);
        require(savedRoom && actual == expected, "fixed original-DLL room readback");
        if (expected == ENVIRONMENT_ROOM)
            require(actual != originalRoom, "ROOM differs from original");
        if (facadeQuery)
            require(MilesStartup::signedValue(reply.result.return_bits) == actual,
                    "facade signed room agrees with original DLL");
    }
    void after(const MilesWire::Header &h, const StartupBridge::OwnedReply &reply) {
        const unsigned request = static_cast<unsigned>(h.request);
        if (request == 5) {
            require(backend.driver != 0, "actual driver before observation");
            originalRoom = ::AIL_room_type(backend.driver);
            savedRoom = true;
            printf("original_room=%d\n", originalRoom);
            require(originalRoom != ENVIRONMENT_ROOM, "initial ROOM would not discriminate setter");
        } else if (request == 6) {
            MSS_MC_SPEC spec = MSS_MC_MONO;
            ::AIL_speaker_configuration(backend.driver, 0, 0, 0, &spec);
            require(spec == MSS_MC_STEREO && reply.result.value[3] == 2, "actual stereo output");
        } else if (request == 7 || request == 16) {
            position(request);
        } else if (request == 8) {
            F32 x = 0, y = 0, z = 0;
            ::AIL_listener_3D_velocity(backend.driver, &x, &y, &z);
            check(request, "velocity.x", x, .001f);
            check(request, "velocity.y", y, -.002f);
            check(request, "velocity.z", z, .003f);
        } else if (request == 9) {
            F32 x = 0, y = 0, z = 0, ux = 0, uy = 0, uz = 0;
            ::AIL_listener_3D_orientation(backend.driver, &x, &y, &z, &ux, &uy, &uz);
            check(request, "face.x", x, 1.f); check(request, "face.y", y, 0.f);
            check(request, "face.z", z, 0.f); check(request, "up.x", ux, 0.f);
            check(request, "up.y", uy, 1.f); check(request, "up.z", uz, 0.f);
        } else if (request == 10) {
            check(request, "rolloff", ::AIL_3D_rolloff_factor(backend.driver), .5f);
        } else if (request == 11 || request == 12) {
            room(request, reply, ENVIRONMENT_ROOM, request == 12);
        } else if (request == 13 || request == 14 || request == 19) {
            room(request, reply, ENVIRONMENT_GENERIC, request != 13);
        } else if (request == 15) {
            puts("idle_serve_returned request=15");
        } else if (request == 20 || request == 22) {
            require(backend.shutdown && !backend.started && backend.metadataInputs.retainedBytes() == 6,
                    "actual shutdown retains directory input");
        }
    }
  private:
    Oracle27(const Oracle27 &);
    Oracle27 &operator=(const Oracle27 &);
};
#endif
