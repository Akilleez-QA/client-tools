# Genuine valid-WAV metadata observation

Authorized bounded no-device native fixture. Debug and Release Win32 invoke the original private DLL's actual `_AIL_WAV_info@8` once per process; no AIL_startup, driver, playback or other Miles function. It returns1. Debug and Release native x64 decoder processes never load Miles; they decode the Win32 metadata, check all11 scalar/offset fields against the recorded text, restore pointers into their own retained image and reproduce the44 encoded bytes exactly. All builds use v120 /W4 /WX and exit0.

| Observed field | Value |
|---|---|
| format | 1 |
| data offset | 44 |
| data length | 8976 |
| rate | 22050 |
| bits | 16 |
| channels | 1 |
| channel mask | 0xffffffff |
| samples | 4488 |
| block size | 2 |
| initial offset | 44 |
| null mask | 0 |

Original DLL SHA2560785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe. Known-valid private WAV SHA256ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9. DLL loaded path is verified, both file hashes checked before and after runs. V2 additionally compares the in-memory retained image before/after the genuine call; the comparison passes. V1 evidence is retained separately and was not claimed to check in-memory mutation.

Both returned pointers are inside the retained allocation for this sample. No null pointers or one-past initial pointers were observed, so this does not settle those conservative candidate restrictions generally. This is one PCM WAV, not arbitrary format, malformed-input safety, MP3 support, fidelity, device or gameplay acceptance. WAV_info is not enabled in the actual host dispatcher.

Only authored fixture source, logs, metadata and hashes are publication candidates. DLL, SDK/header, media, fixture binaries and private metadata binary stay private. Evidence: sound-info-vendor-results-v2; reproducible script sound-info-run-vendor.py uses private inputs and existing private SDK include path. No product/worktree changes.
