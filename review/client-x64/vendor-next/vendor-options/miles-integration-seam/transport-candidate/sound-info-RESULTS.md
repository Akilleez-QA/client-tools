# SOUNDINFO metadata component — 2026-09-30

Separate candidate files only. Existing frame codec/registry and its 449-check baseline are unchanged. No Miles calls, SDK headers/binaries copied into the evidence, product edits, commits or pushes.

| Native v120 /W4 /WX | Result |
|---|---|
| Win32 Debug | 92/92, explicit size-above-UINT32_MAX skip |
| Win32 Release | 92/92, same skip |
| x64 Debug | 93/93 |
| x64 Release | 93/93 |
| Host GCC ASan + UBSan | 93/93 |
| Host mutation removing data-extent validation | 87/93; exit1, expected |

`sound-info-native-v2/results.json` binds source hashes to native results. All four native builds have zero warnings/errors. V1 stopped under /WX because a test used constant sizeof(size_t) condition; source logic was unchanged, and v2 uses conditional compilation with an explicit Win32 skip rather than counting an inapplicable test as a pass. V1 remains at C:/miles-sound-info-v1.

Tests include independent 44-byte little-endian expected encoding; signed and high-bit scalar preservation; every truncated prefix; excess bytes; unknown null-mask bits; noncanonical null offsets; data extent ending exactly at retained size; one-byte overflow and UINT32_MAX subtraction bounds; zero-length data at end; initial pointer at end rejection; mapping/restoring real local addresses; unrelated-buffer rejection; output unchanged after rejection. A removed extent check fails six checks including near-UINT32_MAX values. No giant allocation is attempted.

The private genuine Mss.h definition and Audio.cpp3706–3728 were inspected. The current caller retains fileImage through WAV_info/scalar consumption then frees it. It does not consume returned data_ptr/initial_ptr. Full metadata is encoded anyway: pointers become checked offsets into the supplied retained image, with bit0 data-null and bit1 initial-null. The image must remain alive and its identity must be bound by the host's retained-buffer registry; this component does not own it.

Conservative candidate constraints: null data implies zero data length; nonnull initial pointer designates a byte, never one-past. Parent approved these as explicit validation boundaries, not proof that every genuine Miles output follows them. Real valid-format WAV_info runs are required before adopting those restrictions in a host. An out-of-image pointer rejects mapping; it is never silently rewritten or transmitted. Signed metadata uses exact 32-bit representation, not narrowing of host ABI fields.

This does not parse WAV, enable WAV_info in the host, establish malformed-input safety inside Miles, preserve callback timing, or prove audio fidelity. No runtime vendor function was called.

Subsequent separately authorized genuine valid-WAV observation is recorded in sound-info-vendor-RESULTS.md. It does not change the component-suite results above or enable the host opcode.
