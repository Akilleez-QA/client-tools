# Decoder candidate

Fresh detached worktree client-decoder-candidate at782aed355. Production edits only Archive.h and UnicodeArchive.cpp. Server counterpart is a patch file, not applied: server-decoder.patch, preserving existing source/API drift. No commits/pushes.

Each declared payload count is checked against remaining source before raw access or destination modification. Uses existing getSize/ReadException; public ABI and valid encoding unchanged. Zero-size string clears; ByteStream zero appends nothing. Length headers remain consumed if preflight rejects. Unicode compares units to remaining/sizeof(unit) before multiplication, copies via checked ReadIterator::get into an owned Unicode::String, then swaps destination.

Bundled STLport guarantee checked directly: stlport453/stlport/stl/_string.h lines118-124 uses typed _M_start allocation; lines252-257 sized constructor allocates n+1 and fills contiguous n code units; lines445-448 operator[] dereferences _M_start+n. Unicode.h defines unicode_char_t unsigned short and String basic_string thereof. Thus nonempty &decoded[0] refers to appropriately aligned contiguous live code units. Empty storage is never dereferenced. This supports this implementation, not a claim about arbitrary old C++ string libraries.

Prospective oracle:34 explicit assertions over fully initialized small byte arrays, productioncandidateonly; exact verdict+zeroexit, no skip accepted. Odd offset Unicode confirms byte-copy semantics. Incomplete scalar header leaves iterator unchanged; complete declared-length header remains consumed on rejection. Destination unchanged on preflight rejection. Existing wire suite verifies established valid bytes separately.

Open: full decoder/object transactions and callbacks; Unicode writer multiplication check; resource limits against very large otherwise valid messages; native final candidate compile/runtime. No allocation failure injection or unsafe old decoder execution.

Results: focused portable34/34 Win32 and34/34 Win64. Existing wire59/59 Win32 and66/66 Win64. Server patch `git apply --check` succeeds without applying it. Candidate diff check clean. Raw logs/manifests under portable32/,portable64/,wire32.log,wire64.log. Native evidence from earlier85 ByteStream tests does not transfer to this new Unicode decoder implementation.

Native final validation: actual ByteStream, ArchiveMutex and UnicodeArchive plus focused fixture built with v120/bundled STLport in Debug/Release × Win32/x64;34/34 pass in every executable, exit0. PE width checked. Map binds ByteStream::put to0.obj and Unicode Archive::get to3.obj. Uses same recorded genuine LCD-v4 minimum-block MemoryManager/DebugHelp/InstallTimer and core/STLport objects as previous buffer test, a mixed dependency snapshot rather than full client. Sources/libs hashed in native-v1.zip/verified-results.json. Known Debug MM::remove numeric summary is allowed by constrained verifier; no other unexpected output or extra verdicts accepted. Initial exact-single-line runner flags Debug summary, preserved; early verifier invocation before results existed failed harmlessly and was rerun after build completion.

Portable runner is now added immediately after test-byte-stream in existing wire CI matrix, using same Wine prefixes. CI itself has not run remotely. No production base edits, commits, or pushes.
