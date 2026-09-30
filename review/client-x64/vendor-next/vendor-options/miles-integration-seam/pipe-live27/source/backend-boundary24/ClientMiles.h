#ifndef CLIENT_MILES_STARTUP_FACADE_H
#define CLIENT_MILES_STARTUP_FACADE_H

#include <cstdint>
#include <stdexcept>
#include <string>

// Partial, source-level Miles facade. Select one implementation before startup
// and retain it through complete teardown. This is not a vendor ABI declaration.
namespace ClientMiles {
struct DigitalDriver;
typedef DigitalDriver *HDIGDRIVER;

struct OwnedText {
    bool isNull;
    std::string value;
    OwnedText() : isNull(true) {
    }
};

enum class FailureReason {
    Unsupported,
    InvalidArgument,
    InvalidDriver,
    WrongState,
    InputLimit,
    ResultLimit,
    QueryFailed,
    BackendFailed
};

class Failure : public std::runtime_error {
  public:
    Failure(FailureReason reason, const char *message)
        : std::runtime_error(message), reason_(reason) {
    }
    FailureReason reason() const {
        return reason_;
    }

  private:
    FailureReason reason_;
};

// Calls remain separate; configuration and fallback decisions belong to Audio.
// A zero vendor startup result and a null vendor driver result remain values.
// Backend failures throw Failure instead of fabricating either result.
int32_t startup();
void shutdown();
intptr_t get_preference(uint32_t number);
intptr_t set_preference(uint32_t number, intptr_t value);
OwnedText last_errorOwned();
OwnedText set_redist_directoryOwned(const char *directory);

// Explicit adaptation of Audio's bounded 256-byte resource version query.
OwnedText MSS_versionOwned();

HDIGDRIVER open_digital_driver(uint32_t frequency, int32_t bits, int32_t channels, uint32_t flags);

// Only the channel-spec output consumed by Audio. This is deliberately named
// differently: no speaker-position pointer or other outputs are promised.
int32_t speaker_configuration_spec(HDIGDRIVER driver);

// The current pipe implementation supports get1/get42, set42=16/64 and a single
// 22050/16/stereo/zero-flags driver. Unsupported requests fail before encoding.
// Preference width follows the native pointer width; the pipe checks narrowing.
// Driver identities are opaque, local to the selected implementation and valid
// only through that startup lifetime. There is no callback/playback contract here.
} // namespace ClientMiles
#endif
