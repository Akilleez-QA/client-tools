# Automated and native follow-up

Submitted client candidate: `a7954b5e78274ab3a9eb558fa10186697ff5e848`, [PR #25](https://github.com/SWG-Source/client-tools/pull/25), on upstream master `949451032647e45e42c3aaef3f41b132c8af36e3`.

Production remains identical to the earlier `3b00af629` candidate. The added workflow tests Win32/x64 Debug/Release real headers and pinned upstream controls, with 14 classifier tests. Only text evidence is uploaded. Debug compiles an object without claiming initialized-engine runtime; Release executes 30 valid-buffer checks.

[Hosted Windows run 36819156114](https://github.com/Akilleez-QA/client-tools/actions/runs/36819156114) passed all four configurations using MSVC 14.44.35207 on Windows 2022. Candidate Release and upstream Win32 Release each pass 30 checks; candidate Debug and upstream Win32 Debug compile; both upstream x64 configurations fail with exactly the expected two ambiguity diagnostics and are not executed. Root downloaded and inspected all eight results and the recorded artifacts.

The [first hosted run](https://github.com/Akilleez-QA/client-tools/actions/runs/36818934854) failed before execution with C2732: the legacy `snprintf` declaration preceded the modern CRT's C-linkage declaration. The fixture now includes `<stdio.h>` before the real foundation header. No production header is rewritten, replaced or skipped. This resolves this fixture's header-order conflict; it is not general modern-MSVC support for the client.

The changed fixture was rerun natively with VS2013: candidate Win32/x64 Release pass 30 checks each; both candidate Debug configurations compile; original Win32 Release passes 30; original x64 has the strict expected ambiguity failure. [Summary](native-summary.json) and [unedited commands, hashes and logs](native) record those six checks. All 275 files in each reused header checkout were compared with the pinned Git input blobs. This was a header-probe rerun, not another whole-library build.

The [previous exact-candidate Win32 consumer builds](https://github.com/Akilleez-QA/client-tools/blob/fd42934b0ebf3849fd1a7668a480a45957b06b05/review/client-x64/pr-ready-next/imemmove/native-consumers/RESULTS.md) still describe unchanged production source: sharedFoundation/sharedFile/clientGame, zero errors, 0/0/5 retained warnings. Whole-library x64 configuration and complete-client acceptance remain separate work.
