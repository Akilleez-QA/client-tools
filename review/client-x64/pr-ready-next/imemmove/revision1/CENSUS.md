# Scoped caller census

Candidate: `9eadbbb` on `94945103`; four files, +7/-7 lines. `caller-census.txt` is a tracked-source `git grep` over `src/engine` and `src/game`, including whitespace before the opening parenthesis. It is not a proof about generated or external consumers.

The five renamed calls are TCPQueue.cpp138/213 (`TCPVector::Size`, int in TCPQueue.h47), Iff.cpp621/623 (`lengthToEnd` and `lengthToEnd+size`, both int), and Md5.cpp119 (`bytesToCopy`, int). Their source expressions stay unchanged. The helper's two DEBUG_FATAL pointer assertions remain; this is not a checked length-range helper and adds no negative-length protection.

Remaining first-party calls: DirectInput.cpp1152 multiplies by sizeof, producing size_t; UiBuilder/ImportImageDialog.cpp701 uses strlen+1, producing size_t; DebugWindow/debugWindow.cpp370 uses an int expression but that standalone source includes windows.h, not the shared foundation overload. It remains a CRT call.

External STLport453 has pointer differences in stl/_algobase.h149/184 and size-based char_traits.h166. These remain memmove calls, not renamed engine helper calls. On Win32 ptrdiff_t is int, so removing the globally overloaded helper can change Debug-only pointer assertions for such external calls; valid-buffer Release behavior is the tested scope. No null-pointer or invalid-length behavior was executed or promised unchanged. On x64 the old helper body itself and the ptrdiff_t expression both produce native C2668; the candidate avoids that overloaded name.
