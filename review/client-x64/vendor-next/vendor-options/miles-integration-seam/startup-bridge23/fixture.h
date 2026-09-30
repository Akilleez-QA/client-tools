#ifndef STARTUP_BRIDGE23_FIXTURE_H
#define STARTUP_BRIDGE23_FIXTURE_H
// Test-only comparisons and preference restoration. Does not own startup,
// shutdown, driver creation or transport. Backend provides no oracle API.
struct FixtureOracle {
    Backend &backend;
    MilesStartup::Reply dot, miles, expectedError;
    bool saved;
    SINTa initial, expectedPreference;
    unsigned beforeInvocations;
    size_t beforeBytes;
    char version[256];
    explicit FixtureOracle(Backend &owner)
        : backend(owner), saved(false), initial(0), expectedPreference(0), beforeInvocations(0),
          beforeBytes(0) {
        require(MilesStartup::copyText(::AIL_set_redist_directory("."), dot), "direct dot text");
        require(MilesStartup::copyText(::AIL_set_redist_directory("miles"), miles),
                "direct miles text");
        require(dot.text != miles.text || dot.result.null_mask != miles.result.null_mask,
                "discriminating directory oracle");
        std::memset(version, 0xa5, sizeof version);
        AIL_MSS_version(version, sizeof version);
        require(std::memchr(version, 0, sizeof version) != 0 && version[0],
                "original macro version oracle");
    }
    ~FixtureOracle() {
        if (saved && backend.started) {
            ::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT, initial);
            puts("fixture emergency preference restore");
        }
    }
    void before(const MilesWire::Header &h, const MilesWire::Call &c) {
        beforeInvocations = backend.metadataInvocations;
        beforeBytes = backend.metadataInputs.retainedBytes();
        if (backend.started && (h.opcode == MilesWire::AIL_get_preference ||
                                h.opcode == MilesWire::AIL_set_preference))
            expectedPreference = ::AIL_get_preference(c.value[0]);
        if (h.request == 9) {
            // Static storage persists through normal and emergency Backend shutdown.
            ::AIL_set_error("startup bridge23 first");
            require(MilesStartup::copyText(::AIL_last_error(), expectedError),
                    "direct first error snapshot");
        }
        if (h.request == 10)
            require(MilesStartup::copyText(::AIL_last_error(), expectedError),
                    "direct second error snapshot");
        if (h.opcode == MilesWire::AIL_shutdown) {
            require(saved && backend.started, "fixture restore before actual shutdown");
            ::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT, initial);
            require(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT) == initial,
                    "fixture restore readback");
            saved = false;
            require(backend.metadataInputs.retainedBytes() == 8,
                    "directory inputs alive before shutdown");
            puts("fixture preference restored before shutdown");
        }
    }
    void after(const MilesWire::Header &h, const MilesWire::Call &c,
               const StartupBridge::OwnedReply &reply) {
        const MilesWire::Result &r = reply.result;
        if (h.request == 5 || h.request == 15 || h.request == 18 || h.request == 19 ||
            h.request == 22) {
            require(backend.metadataInvocations == beforeInvocations,
                    "rejected before metadata adapter");
            require(backend.metadataInputs.retainedBytes() == beforeBytes,
                    "rejection preserves retained input budget");
            if (h.request == 15)
                require(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT) == expectedPreference,
                        "rejected preference unchanged");
            printf("rejected_before_adapter request=%I64u retained=%u\n", h.request,
                   static_cast<unsigned>(beforeBytes));
            return;
        }
        require(r.transport_status == StartupBridge::Success, "fixture successful operation");
        if (h.opcode == MilesWire::SessionVersion)
            require(reply.text.size() == std::strlen(version) + 1 &&
                        !std::memcmp(&reply.text[0], version, reply.text.size()),
                    "framed version equals actual macro");
        if (h.opcode == MilesWire::AIL_set_redist_directory) {
            const MilesStartup::Reply &expected = h.request == 3 ? dot : miles;
            require(reply.text == expected.text && r.null_mask == expected.result.null_mask,
                    "direct directory equality");
        }
        if (h.opcode == MilesWire::AIL_startup) {
            require(backend.started, "real startup success");
            initial = ::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT);
            saved = true;
        }
        if (h.opcode == MilesWire::AIL_get_preference ||
            h.opcode == MilesWire::AIL_set_preference) {
            require(MilesStartup::signedValue(r.return_bits) ==
                        static_cast<int64_t>(expectedPreference),
                    "signed direct preference return");
            if (h.opcode == MilesWire::AIL_set_preference)
                require(::AIL_get_preference(c.value[0]) == static_cast<SINTa>(c.value[1]),
                        "actual set preference readback");
            printf("signed preference request=%I64u result=%I64d\n", h.request,
                   MilesStartup::signedValue(r.return_bits));
        }
        if (h.opcode == MilesWire::AIL_last_error) {
            require(reply.text == expectedError.text &&
                        r.null_mask == expectedError.result.null_mask,
                    "direct owned last-error snapshot");
            if (h.request == 9) {
                ::AIL_set_error("startup bridge23 changed");
                require(reply.text == expectedError.text,
                        "host text survives next vendor mutation");
            }
        }
        if (h.opcode == MilesWire::AIL_speaker_configuration) {
            MSS_MC_SPEC spec = MSS_MC_MONO;
            ::AIL_speaker_configuration(backend.driver, 0, 0, 0, &spec);
            require(r.value[3] == static_cast<uint32_t>(spec) && spec == MSS_MC_STEREO,
                    "direct real-driver speaker output");
        }
        if (h.opcode == MilesWire::AIL_shutdown || h.opcode == MilesWire::SessionClose)
            require(backend.shutdown && !backend.started &&
                        backend.metadataInputs.retainedBytes() == 8,
                    "retained paths through actual shutdown and close");
    }
  private:
    FixtureOracle(const FixtureOracle &);
    FixtureOracle &operator=(const FixtureOracle &);
};
#endif
