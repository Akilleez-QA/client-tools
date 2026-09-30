# Proposed source shape

Use plain `ClientMiles` functions selected at link/composition time. The names and call boundaries follow the installed Miles API; existing Audio policy still decides order, configuration and fallback. There is no generic audio object or command bus in the public contract.

```cpp
namespace ClientMiles {
struct DigitalDriver;
typedef DigitalDriver *HDIGDRIVER;

struct OwnedText { bool isNull; std::string value; };

int32_t startup();
void shutdown();
intptr_t get_preference(uint32_t number);
intptr_t set_preference(uint32_t number, intptr_t value);
OwnedText last_errorOwned();
OwnedText set_redist_directoryOwned(const char *directory);
OwnedText MSS_versionOwned();
HDIGDRIVER open_digital_driver(uint32_t frequency, int32_t bits,
                               int32_t channels, uint32_t flags);
int32_t speaker_configuration_spec(HDIGDRIVER driver);
}
```

The owned suffix makes pointer-return adaptation visible. Null and nonnull-empty text remain distinguishable; no hidden last-frame storage. MSS_versionOwned models only Audio's bounded256 query. The observed preference domain is get1/get42 and set42 to16 or64; the public intptr_t value matches the existing private header's WIN64 SINTa, while the pipe adapter checks representability and the narrower supported domain before encoding. Returned x86 preference values are sign-extended, never zero-extended. The concrete pipe adapter may reject other inputs explicitly. It must not silently normalize them.

The driver is an opaque local typed identity. Only the private pipe implementation maps it to a wire handle. Null remains the real vendor-open failure result; a channel failure throws a named ClientMiles failure instead. The explicitly named speaker_configuration_spec adaptation returns only the signed channelSpec value consumed by Audio. The vendor-returned speaker-position pointer and other outputs are not exposed; supporting them later requires its own explicit ownership contract. No Mono/Stereo-only public enum is presented as the complete SDK.

Public exceptions distinguish invalid/unsupported arguments, wrong lifecycle, invalid driver, text/budget failure and backend/query failure without exposing transport status numbers. Exception behavior is experimental failure policy; there is no claim that existing product call sites already handle host crashes correctly.

A private pipe session is selected once before startup and owns the channel until shutdown and protocol teardown complete. It contains Hello/SessionClose, process setup and wire IDs. It does not perform extra Miles startup/shutdown calls or choose stereo fallback. Source-only tests can bind a test channel through this private construction seam; a test-only linked implementation demonstrates that the public sample compiles with every pipe source physically absent. Such a substitute is never a production backend or evidence of fidelity.

This is a source-oriented migration facade resembling a future direct SDK implementation. The existing private Mss.h (SHA966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e) already supports WIN64 and defines signed64 SINTa. It is the concrete source reference. A private direct native_miles64.cpp will delegate these calls and be compiled under v120 x64 against that header without vendor linking or execution. The matching x64 binary is unavailable; link/runtime compatibility, playback, callbacks and Bink are not claimed. No vendor header body is copied into this packet.
