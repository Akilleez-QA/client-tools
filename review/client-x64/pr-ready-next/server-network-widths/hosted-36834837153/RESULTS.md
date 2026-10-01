# Initial server Windows network check: failed

[Hosted run 36834837153](https://github.com/Akilleez-QA/src/actions/runs/36834837153) tested exact fork head `402e5da346ef24636a0734bcae558f3863d5976f` with the server CMake-derived includes/flags, MSVC C++17, and genuine Windows SDK. **4/20 outcomes passed**; tracked inputs remained unchanged and no runtime executions occurred.

All four Sock.cpp cases compiled. All TCP candidate/control cases hit Winsock 1.1/2 declaration collisions: foundation's FirstPlatform.h includes windows.h before OverlappedTcp.h includes winsock2.h. Failed candidate compilations correctly prevent acceptance of their negative controls. A second runner issue was also found: modern MSVC reports the actual GetQueuedCompletionStatus call's start line, while the original classifier expected its closing line.

The source prerequisite and classifier correction remain separate commits. This failed run is retained unchanged; it does not establish Windows TCP compilation. [Summary](summary.json), [case results](results.json), and [raw text evidence](text-evidence.zip) contain the observations. No SDK source or compiled binaries are included.
