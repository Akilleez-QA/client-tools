# Fix x64 UI, tag and mesh native-size mismatches

Six small root-cause commits address native-width/overload failures without changing the underlying UI, tag or mesh algorithms:

- Select `__nop()` on x64 while retaining the Win32 inline assembly.
- Keep nonnegative UI parser offsets as `size_t` and print them with the matching MSVC format.
- Select the chat string's position/count/character insert overload explicitly.
- Preserve the combat parser's string position and `npos` width.
- Retain `strlen`'s native width when forming the existing four-byte tag.
- Match five Debug mesh range-check zero arguments to their `size_t` operands, retaining the checks.

Based directly on master `949451032647e45e42c3aaef3f41b132c8af36e3`; head `9396a5181` (full identity in the receipt). Seven production source files, +19/−11; no tooling. All added/removed lines match the six original commits. Tag and mesh are independent non-UI consumers, preserved as separate commits rather than presented as UI prerequisites. Published UI-pool alignment and ShellExecute fixes are excluded.

[Historical UI build evidence](https://github.com/Akilleez-QA/client-tools/blob/39dc3c354246e4273d6ce940932985bbc23c59c7/review/client-x64/next-build/RESULTS.md) records native UI project builds in Win32/x64 Debug/Release. It explicitly retains the blocked standalone formatter-runtime probe; this package makes no formatter runtime claim.

[Historical native-size evidence](https://github.com/Akilleez-QA/client-tools/blob/56ecc29fc95c62d10241b6cac0d8d9e713961db1/review/client-x64/allocator-math-next/RESULTS.md) records the chat/combat source changes and 4098 actual-header tag values per ABI matching stock. The associated Debug consumer checks cover the actual mesh translation unit and DirectInput; the old x64 Audio compile remained blocked on its separate Miles callback signature. There is no dedicated chat/combat runtime claim here.

Those results use recorded integrated source/dependency snapshots, not a fresh build of this master-based package. No builds or runtime tests were repeated during packaging. Bounded tag inputs do not establish giant-string or null-input behavior; retained Debug range checks do not repair their preexisting narrowed diagnostic display formatting. This is not general UI/gameplay or complete x64 qualification.
