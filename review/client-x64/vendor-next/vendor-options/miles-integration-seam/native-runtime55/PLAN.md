# Native runtime55: five object-only inputs, preparation only

No staging, compiler, VM probe, link, DLL load, test supplier or engine workload has run for55. Active native54 work is untouched. A separately reviewed exact driver invocation is required before the first gate. Preserve the first failure and all logs; no source repair/retry in that run.

## Exact matrix

| Architecture | Actual new source | Native evidence required |
| --- | --- | --- |
| Win32 / x86, COFF 0x14c | host-runtime50/host_file_runtime.cpp | Defined Runtime invoke/fatal; unresolved Scope41 snapshot, real49 token/transaction, Endpoint and actual codec/decoder calls |
| Win32 / x86, COFF 0x14c | host-runtime50/host_sdk_callbacks.cpp | Actual possessed Mss.h, all four existing SDK typedef static_asserts; exactly `__imp__AIL_set_file_callbacks@16` among undefined AIL symbols; unresolved actual Runtime invoke |
| Win32 / x86, COFF 0x14c | host-runtime50/host_install.cpp | Actual install decoder/reply encoder, Scope41 and SDK-installer references; defined installAdmitted |
| AMD64, COFF 0x8664 | client-runtime53/client_file_runtime.cpp | Real EngineFileWorker create/start declarations and selected services/mapper/Endpoint references; defined launch/prepare/publish/returned |
| AMD64, COFF 0x8664 | callback-control45/host_association_mapper.cpp from53 | Actual owner receive/poll/acknowledge and protocol48 expectation/ACK validation references; defined new nextUnqueuedReply and receiveControl |

Those are the only five translation units. Candidate headers are copied independently into host/client subtrees to preserve exact frozen parents, including differing inherited implementation families. No FileInvocationJob.cpp, EngineFileWorker.cpp, portable_job.cpp or other supplier implementation is copied or compiled. No source is altered to make this gate pass.

## Identity and toolchain

host50 source manifest is7710275d8c5d35f68b08478f3c003b15324fcbfe936ecb6c5d3dfddff568907b; client53 is19d7d3376d2a8ea73fc7282c7c0bfe75d559d95b9845785119e2eff5ede00aad. Independent source reviews were read;53 caller-TLS audit does not identify a mandatory normal-path TLS fix. It does identify optional diagnostic/profiler and teardown limits that this object gate cannot resolve.

The possessed SDK header is copied only from `native-file-callbacks35/private-inputs-v1/snapshot/src/external/3rd/library/miles/include/Mss.h`, SHA256966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. No SDK retrieval or redistribution. Its Win32 AILCALL is stdcall; the gate pins the exact expected decorated import rather than accepting arbitrary strings containing the export name. The private SDK/header bytes stay local/VM and are excluded from curated results.

Reuse actual host49 read-only-probed and subsequently gate-verified v120 x86/AMD64 cl/dumpbin/vcvars SHA identities, copied unchanged in private-inputs-v1/toolchain.json. No new VM tool probe is necessary during55 preparation. When authorized, runner selects the corresponding vcvars environment, rehashes the selected actual tools, and fails before compilation if identity differs. Tools are rehashed afterward.

Flags are unchanged from native-host49: actual modern MSVC runtime, /c /W4 /WX /EHsc /MTd /Od /Ob0 with inherited strict flags. Forced per-architecture header requires _MSC_VER1800 and expected target/pointer width. No warning suppressions or compatibility macros. Actual /showIncludes must show pinned v3 headers and MSVC modern memory header; STLport and engine paths are forbidden. Mss.h is permitted only for host-thunks and only at the exact staged pinned SDK path. Compile diagnostics, even failure diagnostics, are retained verbatim.

## New evidence versus prior receipts

Host49 already compiled token/transaction/protocol objects on both architectures;55 does not rebuild or link them. Earlier mapper/owner/job/component receipts do not cover53's thread composition or nextUnqueuedReply.55 compiles the new caller objects against exact headers and inspects their real decorated references. This new SDK-thunk object gate is the first evidence sought here that host50's four functions have the actual Win32 SDK types and import the actual setter declaration. It is not native64 SDK evidence, a linked call graph, or proof of original DLL behavior.

## One future approved execution

After parent review only: `python3 native-runtime55/run-approved-native-v1.py --approved-five-objects`.

Driver requires fresh local native-evidence-v1 and fresh VM C:/native-runtime55. It refuses an already-running compiler rather than disturbing another gate. It pins the frozen input manifest and exact remote runner, verifies clean unchanged product HEAD, stages one archive, executes remote runner once, then collects raw commands, compile logs, observed include hashes, decorated symbol logs and object hashes/machines. Objects/PDB and SDK stay private on VM. All frozen inputs are verified before/after; system headers are single-time observations, not a system-header post-hash claim. No tests are run; no engine suppliers, SDK DLL or linker are executed.

Success proves only five scoped source/type/object-reference checks. It cannot establish SetEvent/wait synchronization behavior, worker engine TLS/allocator execution, paired installation, Session/LiveChannel integration, normal shutdown, quiescence or file-close obligations.

`IDENTITIES.json`, `provenance.json`, `private-inputs-v1/input-manifest.json` and `runner-from49.patch` provide reviewable identities and runner delta.
