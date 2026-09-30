# Native math checkpoint — 2026-09-30

The parent owns acceptance and commits. No new PRs. These are actual v120 Windows probes with real production translation units, actual project include/define metadata, actual compiled project dependency libraries, SDK imports and CRT. No symbol stand-ins. Each runner records source/probe/metadata/library hashes and link commands. Initial failures and revised probe versions remain separate.

## SseMath

Original Win32 disassembly and the six-build tiny probe establish the compiler-sensitive cross-asm-block register lifetime bug described in `ssemath-clobber-analysis.md`. Production Win32 remains unchanged. The diagnostic reload control is explicitly not stock. Across 33,280 cases per configuration it agrees with x64 on finite, subnormal, extreme and discarded-lane categories including recorded MXCSR. Exceptional NaN representation differences remain. No callers of the four arithmetic APIs were found; no gameplay failure or universal equivalence is established.

## Transform

Final runner output: `C:/transform-next-v6-agent`, probe `transform-probe-v2.cpp`. Each of Debug/Release Win32 stock, Win32 candidate and x64 candidate recorded 1,024 cases. Win32 candidate records are byte-identical to stock in both configurations. Every run reports zero alias/control failures. Debug's entire corpus matches x64 exactly. Release's768 finite cases match; 136 exceptional records differ in 464 value words, all pairs being NaNs with different payloads. No recorded flag or non-NaN value differences. Its strict all-words comparator retains exit 1 for Release; this is not presented as a universal bit-identity pass. Dispatch is bound to the real kernel in the diagnostic TU; normal startup/dispatch selection and game scenes are not tested. Cases include intentionally unaligned transforms, output aliases with either/both inputs, all rounding directions and FTZ off/on.

## Collision normalization

Final runner output: `C:/collision-sqrt-v5-agent`, probe `collision-sqrt-probe-v2.cpp`, copied candidate CollisionUtils.cpp source hash 0138c32cbbf176d30fa5d92f85f8364c01bcba826e0e5d2fc461e4146a84f81e. The source-only authorized product overlay has a before/after manifest at `C:/collision-library-v1-agent`; all four genuine sharedCollision project builds return 0. TestLineTwist4's map binding is checked against the probe object containing the actual TU.

Debug and Release each record 8,192 cases for stock Win32, candidate Win32 and x64 candidate. Win32 is unchanged. Every value, line-twist classification and MXCSR word matches across ABIs, including this exceptional corpus. The sole differing record field is the separate x87 status word, present on Win32 versus the explicit zero field on x64:7,212 records/configuration. The comparator intentionally treats these different hardware-unit fields as observations rather than requiring the nonexistent x64 x87 path. Both finite-contract comparisons return 0. This is a sample, not exhaustive FSQRT/SQRTSS equivalence or a gameplay acceptance test. Win32 oracle explicitly uses PC64 and aligned rounding controls; DAZ remains off in this probe.

## Probe correction and dependency boundaries

Version 1 Transform/Collision returned synthetic float bit patterns by value. Native Debug revealed mismatched signaling-NaN inputs because Win32's float return passes through x87. Version 2 copies raw bits into output references; it changes no implementation or acceptance threshold. `probe-input-correction.json` binds both versions. The original failed input comparisons remain.

Initial actual-TU link failures were resolved with genuine project dependencies, not fake declarations. The original Win32 Debug zlib project emits to C:/compile/win32/zlib/Debug/zlib.lib; v120 Build succeeds with 0 errors and 0 warnings. SHA256 487833b41d1fc71efcbce895736116b521803cd68a8ed582ba313adba0c74e09. Win32 Debug linker warning LNK4075 records that EDITANDCONTINUE is ignored with optimized linking; no dependency or numerical failure is hidden by it.

SseMath Windows source/header originally matched across client/server byte for byte, so the candidate was mirrored uncommitted. No Linux implementation changed. Skeletal candidate remains paused and untested.

Delivery state: actual native probe binaries built and run; production candidates remain subject to parent review/commits. Highest justified claim: the bounded numerical/alias/control observations above on the recorded v120 builds. Required runtime observations: representative client scenes and integration behavior; exceptional SseMath/Transform distinctions require explicit disposition. Parent controls next tests.
