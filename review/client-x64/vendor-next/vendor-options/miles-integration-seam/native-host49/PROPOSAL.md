# Native host49 object gate — prepared, not compiled

Prepare six new objects: file_tokens.cpp, reply_transaction.cpp, and callback-protocol48/file_protocol.cpp, each with actual v120 Win32 and AMD64. Sources and their dependency closure are byte-identical to the tested frozen host49 candidate; no portable tests or test-only terminate handlers are staged. None of the portable executable or prior native objects is reused. No link, executable run, SDK header/load, EngineFileWorker, engine allocator or product source change.

## Actual tool selection

A read-only probe ran the available vcvarsall.bat with x86 and amd64 in separate subprocesses, then `where cl.exe`, `where dumpbin.exe`, file-version reads and SHA256 hashes. No compiler or dumpbin was invoked during preparation, and nothing was uploaded/staged on the VM. Raw probe is tool-probe.json; its script is probe-tools.ps1. The observed tools are actual v120 compiler18.00.40629.0 and dumpbin12.00.21005.1 in VC/bin and VC/bin/amd64. Exact separate per-architecture path/hash maps are staged in toolchain.json and compared to the tools selected by vcvars at the future gate. Case-insensitive normalized Windows paths are used for identity comparison; hashes remain exact.

## Flags and object inspection

Retain native47 flags with one explicit change: /Ob0 instead of /Ob1, keeping /Od, /W4 /WX, /EHsc, /MTd, /RTC1, /Zi and the same existing definitions. This disables inline expansion so used existing registry methods have inspectable emitted symbols. No warning suppression or native-header compatibility macro is added. Separate forced guards require actual _MSC_VER1800 and _M_IX86 without _WIN64, or _M_X64 with _WIN64, plus the matching pointer width.

For every object require COFF machine0x14c (Win32) or0x8664 (AMD64), successful compile and dumpbin, exact pinned candidate registry/protocol include hashes (plus file-channel/protocol-helper headers for their dependents), and no Mss.h, engine, STLport or snapshot headers. System-header hashes are single-time /showIncludes observations, not a before/after attestation. All staged inputs and compiler/dumpbin/vcvars binaries are hashed before/after.

Raw symbol checks use native47's unchanged parser, operating on decorated symbol tokens rather than demangled trailing descriptions:

- file-tokens must define its token methods and the used ResourceRegistry reserve/publish/cancel/resolve/beginClose/retire methods. These are emitted definitions from the real pinned header, not a standalone registry library or proof of a linked call graph.
- reply-transaction must reference actual FileTokens operations, file-channel decodeReply/copyRead, and protocol48 expectFileAck/encodeFileConsumptionAck; it must define consume/ack/result/write-completion methods.
- file-protocol must reference real bounded/vector-independent Call/Result codec entry points and actual validated Request accessors, and define install/ACK/stream-parent validators.
- All objects reject undefined AIL_ references. This is not an SDK-thunk ABI check; no Mss.h enters this gate.

Stop at the first compiler, header, machine or symbol failure, preserve logs, and do not retry, suppress warnings or silently change the source. A missing required inline definition is a preserved gate failure requiring review, not permission to loosen the oracle after the fact.

## Prospective invocation and evidence

Fresh remote destination: C:/native-host49. After explicit parent approval only, the local driver is invoked with --approved-six-objects; it pins the private input manifest and runner, checks the untouched product HEAD/clean state, uploads only this private source closure and staging/collection scripts, and invokes the remote run-native.py once with --approved-six-objects. The remote script also refuses any other invocation or an existing results directory.

Architecture order is x86 then amd64, three units each. Compile/dumpbin commands, logs, actual includes, decorated symbol tables, object hashes/machines, input/tool before/after identities and overall status are curated; .obj/.pdb remain private on the VM. Only logs/JSON/command evidence is downloaded. The collector rechecks objects without executing them. Preparation itself has made no remote directory or archive upload and has run no build.

A successful future gate would establish these six native source/object compatibility observations and dependency references. It would not establish linked behavior, native64 API availability, SDK callback calling convention, actual installation, Endpoint ownership, vendor result fidelity, game runtime, or cleanup safety. Parent review and separate approval are required before compilation.
