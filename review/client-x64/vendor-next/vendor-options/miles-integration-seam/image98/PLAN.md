# image98 prospective portable client-path gate

Source/plan only. No compilation or test execution authorized or performed. Production93 and86 remain unchanged. This author participated in production93; this is test authoring, not an independent production review.

`tree/` is the exact quoted-include closure of frozen93 Core/Session over86, plus the actual registry, BufferUpload, codec, metadata wire, session-version and reentry implementations. `origins.json` identifies every source. The ONLY replaced production dependency is client-runtime53/client_file_runtime.h: the labeled test supplier has a failure counter and forbidden prepare(), no Windows thread, publish/returned, file worker, ACK join or Endpoint. `compat.h` scopes portable Windows/MSVC/calling-convention macros around the unchanged70 header after stdint inclusion, then undefines them. This gives no native ABI evidence.

`tests.cpp` includes the unchanged actual PipeCore.cpp, which supplies real Core::file_type and Session behavior. Scripted Channel checks exact fields, encodes/decodes actual Call frames, returns actual encoded Result frames through real typed reply and owner validation, and owns real ResourceRegistry plus BufferUpload storage. It does NOT execute Backend::executeUpload, LiveChannel, the Windows host or SDK. Its charged-byte counter is an oracle/model; it is not evidence of actual host budget accounting. A fake classifier value is explicitly injected. No public guarded-wrapper fatal reporter is executed: this is Core/Session scope.

Independent fixed oracles:

* Small operation list is numeric `[4097,4098,4099,9,4100]`; large is `[4097,4098,4098,4099,9,4100]`. It is not generated from production code or recorded actual output.
* Large input has literal length1,048,459, expected chunks1,048,440 and19 at offsets0 and1,048,440. Boundary bytes are independently set and whole reconstructed contents compared with an untouched input copy. Expected fixed Call offset136 and full frame bound1,048,576 are checked separately.
* Input return bits0,0xffffffff,0x80000000,37 compare against literal results0,-1,INT32_MIN,37. No production signed conversion computes the expected answers.
* Explicit budget14 rejects8-byte input before Channel and accepts sequential7-byte operations; actual Session reuse and model retirement/counter restoration are checked. Cross-frame success uses exact2N budget2,096,918. This does not establish host allocator capacity, allocation-failure behavior or total process RSS.
* Supplier calls actual owner validation with an incompatible phase after each valid non-Begin result. Malformed Begin and malformed Release are generic-envelope-valid but rejected by the actual typed decoder, whose sentinel output remains unchanged. Known refused Release is decoded normally and rejected by actual Session status handling.
* Every negative query leaves output777 and returned=false, retains scripted storage, checks input unchanged, marks actual Session uncertain and increments substituted runtime failure observation. A repeat Core call must not call Channel again. These tests do not assert that a real host necessarily retained storage after a Release actually executed but its reply was lost.
* CHECK sets persistent anyCheckFailed before throwing. Expected-rejection helpers catch all exceptions and then reject any persistent assertion failure. Main has std::exception and catch-all failure exits. There is no expected-failure branch that can silently swallow a check failure.

Prospective one-binary/five-process gate (NOT run):

1. `success`: four scalar queries, then cross-frame query. Two named markers.
2. `budget`: pre-send invalid/over-budget cases and two exact-budget queries. One marker.
3. `malformed-begin`: no classification or release, terminal/no retry. One marker.
4. `refused-release`: classification observed by supplier but not returned by Core, terminal/no retry. One marker.
5. `malformed-release`: generic reply accepted, typed shape rejected, no ordinary return, terminal/no retry. One marker.

Each process gets a fresh selected Session. The fixture uses aligned static placement storage and manually clears test-owned Session members because the real Session destructor deliberately terminates. It never invokes production teardown or claims cleanup proof; supplier-owned component allocations are ordinary local RAII. No engine memory manager, real SDK supplier library, VM or native runtime is involved. Sanitizers must retain leak detection; no suppression or forced successful exit is proposed.

Future reviewed runner must freeze every source/header, supplier, compatibility file, test, command and itself before its first build. Proposed strict compiler flags: C++11, Wall/Wextra/Wpedantic/Werror, O1/g, ASan+UBSan, no sanitizer recovery, frame pointers. Build TUs: tests.cpp (includes actual Core), codec.cpp, buffer_upload.cpp, session_version.cpp, metadata_wire.cpp, invocation_guard.cpp. Use compat.h preinclude. Do not compile actual Windows Runtime or host handler, and do not imply their absence is native source validation.

Run the five literal modes once in the order above, require every named marker exactly once in its own process and one assertion summary per process, stop at the first nonzero build/run or missing/duplicate marker, retain all raw output, and check all frozen input hashes afterward even on failure. No repair/retry. Tool identity and exact runner are deliberately not frozen here because this request authorizes test source/plan only; a later runner preparation/review is required before execution.

Remaining separate host work: direct actual Backend handler validation, partial/replayed uploads, allocator limits/failure, actual registry stale generation routing, host terminal refusal, private bootstrap parsing, Windows Endpoint/admission/ACK, and genuine SDK behavior. This gate must not be labeled full upload integration or operational Audio adoption. Any independent review finding against93 must create an explicit revised source base and refreeze; never silently edit this staged93 closure.
