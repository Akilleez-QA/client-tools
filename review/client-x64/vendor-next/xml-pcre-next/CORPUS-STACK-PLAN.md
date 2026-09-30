# Separate diagnostic stack experiment

Keep v1 and v2 unchanged. v2 enables CRT %n only inside the trusted upstream test driver. The observed x64 Debug testinput2 overflow occurs with the same 1 MiB reserve / 4 KiB commit as the actual Win32 game executables; x64 game response files specify no alternative reserve.

Before running v3, set only pcretest.exe link /STACK:8388608,4096 for all six candidate/stock ABI/configuration combinations, using identical libraries, input files and driver. Repeat corpora 1,2,4,5. No production settings change. Passing at 8 MiB establishes bounded algorithm output coverage only; the 1 MiB x64 Debug stack limit remains a recorded compatibility limit. Compare exact outputs first; retain architecture Study size metadata differences separately, never mask matching differences. Locale corpus3 remains skipped because exact fr locale is unavailable.

## Follow-up declared before execution
Parent requests next power-of-two 2 MiB reserve / 4 KiB commit diagnostic, same six variants, unchanged libraries and four upstream corpora. Keep1MiB failures and8MiB successes intact. No production edits. This tests smallest next reserve, not arbitrary pattern expansion.
