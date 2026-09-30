# SessionVersion21 result and handoff

The bounded component passed native v120 Debug/Release checks on Windows: the x86 host called the actual private Windows `AIL_MSS_version` macro with a 256-byte buffer against the original DLL, and the x64 consumer copied the resulting owned wire text unchanged. The observed text is **7.2a**, five bytes including NUL. A build whose `MSS_VERSION` was deliberately set to `SV21_COMPILE_TIME_POISON` still returned **7.2a** in both configurations.

## Contract

`session_version.h/.cpp` provide portable request creation/validation, owned response encoding and checked copying into the actual caller's `char[256]` shape. `session_version_host.h/.cpp` implement only the x86 ANSI Windows query. The SDK macro is invoked by name; its private body is not copied into this component. No AIL function/export is defined or substituted, and no Miles import library is linked.

The existing SessionVersion opcode is used without modifying the frozen schema/codec. Request Call fields are all zero. Header request and lane must be nonzero; causal request and lock lease are preserved, with session admission left to the integrating caller. Reply Result fields are all zero except the codec-generated text span. That span contains 1–256 bytes, exactly one final NUL and no earlier NUL. Only meaningful text plus its terminator is serialized; no pointers or uninitialized buffer tail is transmitted.

`copyReply` validates the frozen frame codec, Reply kind, SessionVersion opcode, exact request/causal/lane/lease context, every otherwise unused Result field, bounded text length and termination before writing. It writes only through the final NUL. Missing/truncated/malformed/mismatched responses return false and leave the entire destination unchanged. The integrating client must propagate this failure and must not construct a string from an unchanged uninitialized buffer.

The host caller must already hold the verified original module for the entire call and exclude concurrent unload. The adapter checks that the SDK's DLL basename resolves to that same module. The probe additionally verifies the mapped path against the launcher's exact hashed path. This contract does not provide loader ownership, session admission or a transport implementation.

## Observed checks

| Surface | Debug | Release |
| --- | --- | --- |
| Native x86 portable wire | 600/600 | 600/600 |
| Native x64 portable wire | 600/600 | 600/600 |
| Actual DLL macro/resource host | 22/22 | 22/22 |
| Poisoned compile-time string host | 23/23 | 23/23 |
| x64 consume normal x86 response | 606/606 | 606/606 |
| x64 consume poisoned x86 response | 606/606 | 606/606 |

Controls cover every truncated request length, each nonzero request payload byte, empty text versus missing reply, maximum 255-character text plus NUL, unterminated local input, high-bit ANSI byte preservation, every truncated result length, context mismatch, nonzero result metadata, malformed/oversized text and output preservation. Host checks establish text ownership after source-buffer reuse and DLL unload. The x64 handoff uses files containing the encoded frame and direct-resource oracle bytes; it is a two-process serialization/copy test, **not a live pipe test**.

The direct oracle is Windows `LoadStringA` on string resource 1 of the held original module. This is a distinct API path but shares Windows, the DLL and resource with the macro. It is not independent vendor validation. The poison control discriminates compile-time substitution even though the ordinary SDK and DLL strings agree.

Every native build used `/W4 /WX`, the original v120 compiler and explicit Debug/Release flags. All eight final builds recorded unchanged source/header/tool/library inputs before and after compile/link, matching discovered header sets, no uncovered observed library-search paths, immediate output PE machine/hash and a stable full matrix. Local source was checked against the frozen native build record afterward. Runtime checked both PE and original DLL hashes immediately before launch and afterward. The launcher ran under Python `-O`; a wrong external receipt pin was rejected before any runtime directory or PE launch. These are explicit checks, not Python assertions.

## Artifact identities

- Source snapshot: `source-v2.tar`, SHA-256 `9df919c78297f91e20db85ceebaa41a1d4319bdda5425826d919e93459bf3040`.
- Final native receipt: `evidence-v2/build-v2/receipt.json`, SHA-256 `da0b0381f67667e030c909f32ae6e1a2fbfd368224de37a294278d24c3a90857`.
- Runtime outcomes: `evidence-v2/runtime-v2/results.json`, SHA-256 `12a3e2ce412c89f9a99632aedeb632158496563a645c1d9a075361cdfdd78c9b`.
- Text evidence archive: `evidence-v2.tar`, SHA-256 `d5bf4eb14e5cb45dd903f99d009ffbf3939c54071a8b3e743de8f12481e67068`.
- Original private DLL: SHA-256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
- Private SDK header: SHA-256 `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`.

| PE | SHA-256 |
| --- | --- |
| x86 Debug wire | c51d162fb5eb771a7191084b3b8d19d04ca378a83ccf47911f7fe14cc6986b47 |
| x86 Debug host | e583eb443740ab1b49b48b51e988e55f70b82403e6a1d92bba24baf43cc392aa |
| x86 Debug poison | c932752c31df88b5b95dc631ec0eec55afdefa3ad1157f66be119baa396c3eba |
| x64 Debug wire | 03ba58dbc4ad7bbb4c9a0f5f1f3ed5c8fa1196093d43f4aa754f770fb34fdd4e |
| x86 Release wire | 05b0306f12ceb380833ba95538f4079db12be9541b3e519bb07dd33be810af92 |
| x86 Release host | bffdb7a02e291659c6c2949abc0ab3a4e98197d1767be4d5dbdf53349486073c |
| x86 Release poison | 89d402fcb2f192acdeeea9aa5032b702296939fd02fb881ae57977aabefdc51c |
| x64 Release wire | 1578670e23d2a589405c8d2e5dbaf7949e1496de0ee60abd38e9e5c8e796da40 |

Native private staging remains `C:/session-version21`, with PEs in `build-v2` and DLL only under `private`. Local evidence is text-only; no vendor binaries, SDK bodies or executables are included. `collect_evidence.py` is a later collection-only script and is explicitly outside the compiled source snapshot.

## Preserved failure and evidence limits

P1 initially failed: `source-v1.tar` and `evidence-v2/build-v1/` retain the first attempt, receipt `ede41494dd16decbfbbb12e2527848aeab07a4a303f0f283759e5a98a1856d09`. v120 treated a signed-char constant-conversion warning in the wire test as an error. Four host/poison builds compiled, four wire discovery passes failed; none of those first-build PEs ran. The replacement high-bit test copies an unsigned object byte and preserves `/WX`. Probe guards were strengthened before runtime. P1b's new snapshot passed; the original failure is not relabeled. An initial inline Python evidence-collection command had a quoting syntax error and launched no test; the saved collection script then collected the evidence successfully.

The resource query uses ordinary DLL loading and thus permits normal DllMain attach/detach; “resource-only” describes the explicit workload. There was no Audio install, Miles startup, device opening, playback, vendor allocator or engine fixture. Native resource text and data copying do not establish callback behavior, transport failure integration, lifecycle concurrency, full bridge correctness, full-client build/runtime or product adoption. No frozen component, product source, upstream repository or PR was changed.

Remaining handoff: parent review; compose SessionVersion routing into the future live host/client boundary; hold original-module lifetime across query; connect a checked response to `Audio::getMilesVersion` with explicit failed-response handling; then test the actual client call through that route. Product changes remain outside this component's authority.

`delivery_state`: built and checked.

`outcome_state`: passed for the exact native resource and file-backed x86-to-x64 handoff surface.

`highest_justified_claim`: the bounded SessionVersion component returns the real original DLL's 256-byte-query result as owned bytes and preserves it in a validated x64 client buffer on the recorded native builds; the poison control detects compile-time substitution.

`required_runtime_observation`: actual client call over the integrated live transport, with module lifetime/session admission and response-failure handling. None remains for the defined component probe (the evidence above passed).

`who_controls_next_test`: parent integration agent under the existing root goal and authority.
