# File channel26 portable result

The first portable build and test run passed: 157 assertions under ASan/UBSan, with warnings treated as errors and all recorded inputs unchanged. The four canonical service bindings compiled separately to an object with unresolved references to the real seam20 open/close/seek/read functions. That object was neither linked nor executed. No SDK, vendor, VM, engine, Audio/ExitChain or real filesystem callback ran.

The authored mapping validates reverse request/reply association and permitted fields, owns filename/read bytes, preserves signed seek bits and uintptr_t local identity, and separates open status from valid local key zero. Tests exercised nonzero open status with key0, failed open with retained diagnostic key bits and no published File identity, negative seek offset/result, short read, EOF, zero-byte read, and an oversized unsigned read result that cannot become successful EOF. Malformed span, extent, field and response cases preserved destination values on rejection.

A test-only allocation hook failed the next allocation in the actual encoder after a scripted successful open. The already-stored status/key0 and context pin survived, the output frame remained unchanged, and no second open or automatic close occurred. A scripted throwing service remained CallThrew and could not produce an ordinary reply or be reinvoked. This demonstrates value retention through that failure; it does not supply the still-missing owner for an unpublished actual file.

The scripted executor used the existing Coordinator to distinguish queued cancellation, running abandonment, observed return and acknowledgement. An invocation retained its local binding/context while its service was executing; failure kept request/callback pins pending, stale acknowledgement and duplicate acknowledgement were rejected, and actual late return could be observed without delivering a successful client result. Duplicate invocation was refused. These are serialized scripted schedules, not evidence of thread safety, real engine affinity, asynchronous cancellation, general ordering or an installed reverse-file transport. The ordinary begun/returned bools require one serialized admitted executor.

| Artifact | SHA256 |
|---|---|
| source-v1.tar,16 members | 714d75ccbc2356bd059dc85d905333a977a526a250924f6b6aeecf2c121316bb |
| source-manifest.json | b064bdbf619920c045f1e5f1b3a9327d3141b76e6d886d651566dc1fd9931425 |
| evidence-v1/results.json | 38b1170ca9bc6139250ce42362cc44df632dae1739986e43e9e9a1e4a331b170 |

Source-manifest paths are relative to the seam/source-archive root. The source archive and evidence bind the exact authored code plus frozen seam20/codec/coordinator dependencies. `evidence-v1` retains commands, output and the canonical unresolved-symbol listing. The separate packet manifest is a flat packet-relative path-to-{bytes,sha256} map rooted at this file-channel26 directory; no binaries, assets, SDK body or nested archive is included in that text packet.

Delivery state: checked. Outcome state: passed for the portable value boundary and named scripted schedules. The highest justified claim is correct mapping within that bounded domain, conditional on an externally admitted serialized executor and supplied live binding. Engine TLS/affinity and ordering with every original callback, file-open publication/rollback, uncertain-disconnect ownership, large/chunked reads, real callback transport and full-client fidelity remain unresolved. In particular, CallThrew may follow a side effect and permits neither retry nor binding retirement. Parent review controls any next integration step; no further runtime is authorized by this result.
