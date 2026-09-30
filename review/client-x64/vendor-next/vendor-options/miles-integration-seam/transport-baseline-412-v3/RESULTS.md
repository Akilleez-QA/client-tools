# Candidate frame codec and registry — 2026-09-30

No product edits, vendor calls, game launch, commits or pushes. This is a component for subsequent genuine host integration, not a working Miles replacement or IPC service.

## Observed

| Build | Result |
|---|---|
| Native VS2013 v120 Win32 Debug | 412/412 |
| Native VS2013 v120 Win32 Release | 412/412 |
| Native VS2013 v120 x64 Debug | 412/412 |
| Native VS2013 v120 x64 Release | 412/412 |
| Host GCC, AddressSanitizer + UBSan | 412/412 |
| Deliberately unchanged generation on retirement | 408/412; exit 1, expected |

Native logs and source digests are in `native-results-v3/`; no binary needs publishing. `run-native.py` reproduces the four native builds in its private directory. Host command: `g++ -std=c++11 -Wall -Wextra -Werror -fsanitize=address,undefined codec.cpp tests.cpp -o tests && ./tests`.

Golden Call/Result/EOS vectors are independently literal bytes, including 64-bit identifiers and high-bit scalar values. Every truncated prefix is rejected. Other checks cover wrong magic/version/kind/opcode, malformed handles, spans into metadata, reversed/overlapping/gapped spans, noncanonical empty spans, excess/trailing length, SIZE_MAX input, exact maximum frame, reserved fields, and output preservation on failure. Registry tests cover kind checking, capacity, null local pointers, close state, stale generations, reuse, permanent exhaustion with a low fixed ceiling, and legitimate file value zero held inside a nonnull local record.

The first 396-check attempt incorrectly treated a changed nonzero slot/generation as structurally malformed. Those values are valid syntax; liveness is registry work. Corrected test uses zero. In strengthening the suite, a Result corruption initially changed the last scalar rather than the span; corrected to actual byte offset 100. Neither mistaken test was hidden as a production defect. Native v1 remains on the VM separately; v2 retained the corrected strengthened tests. V3 replaces the noisy test CHECK do/while macro with a function and passes /W4 /WX in all four builds; v3 is the current source/result binding.

Generation mutation removes `++e->generation` in a scratch copy. The stale ID then resolves after reuse, and exhaustion no longer works; four checks fail. Host logs preserve this discrimination.

## Interface and boundaries

`MilesTransport::ResourceRegistry::resolve(handle, expectedKind, void*& out)` returns only a live, nonnull host-local pointer and clears output on failure. Host adapter may convert that local pointer to its local uintptr_t. Pointers never enter frame encoding. `insert`, `beginClose`, `retire` do not call or free vendor resources. Caller must establish vendor release/callback quiescence before retirement. Configured generation ceiling never increases; exhausted slots are never reused.

Registry is dispatch-thread owned, not synchronized. It does not establish session identity, alias uniqueness, parent/borrowed lifetime, callbacks, retries, or reentrancy. Borrowed sample API operations remain disabled in the separate host subset until stream ownership is enforced. A newly constructed registry is a new session namespace; external session admission must prevent old-session frames reaching it.

Codec validates canonical structural envelopes; it does not establish opcode-specific argument semantics or sequence/lane/lease admission. Call/Result variable spans are bytes then text, contiguous after metadata; empty spans must be {0,0}. Encoder replaces supplied span metadata from explicit payload views. Text encoding and terminators belong to the API adapter. EndOfSample/EndOfStream are Event-only. Reverse-file and buffer controls use Call/Result envelopes, as confirmed with the schema owner. SoundInfo's nested payload is not yet encoded by this component; its dedicated codec is required before enabling WAV_info.

There is no audio output, callback scheduling, shared helper process, actual DLL fidelity, or full-client acceptance evidence here.

## Independent review

The host-dispatch peer found no stale/reuse/exhaustion arithmetic blocker and compiled a concrete registry adapter with eight invalid-input preflight checks per native x86 configuration. No vendor calls were made. Review boundaries: duplicate native pointer identities are permitted (future alias canonicalization requires an owner map); retiring a live entry relies on caller-established quiescence; failed insert leaves the output handle unchanged, so callers must honor its false return. Host adapter rejects borrowed samples.
