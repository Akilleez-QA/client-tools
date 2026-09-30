# Authentic Vivox wrapper compile and private relink

The repository contains `src/external/3rd/library/vivoxSharedWrapper/Vivox.cpp` and headers, but the .sln references an absent .vcproj. Existing main build uses prebuilt x86 archives. Native compiler accepts the unchanged full implementation in Debug/Release on Win32/x64. The exact source/header hashes, commands and object symbols are in vivox-wrapper-source-v1. VIVOX_VERSION=3 matches CuiVoiceChatManager.h; /MT vs /MTd and /Zc:wchar_t- match current consumers. No fake import, replacement SDK or altered lifecycle.

The code retains LoadLibraryA("vivoxsdk.dll"), GetProcAddress for real SDK entrypoints, original failure behavior and version3 shutdown. Building the wrapper does not provide an x64 SDK DLL, prove structure ABI with an available DLL, establish service availability or test authenticated voice.

Native private relink keeps all original91dc inputs except the documented STLport replacement and sourcebuilt wrapper substitution. Release now reaches final LNK1120 with85 unresolved externals (87 references): Miles AIL imports, PCRE allocator globals, libxml2 calls/data and10 LCD entrypoints. Committed later LCD props were intentionally absent from the91dc experiment. Debug first stop is x86 VideoCapture_debug.lib(EncoderConstants1.obj). Raw link responses, provider hashes and /VERBOSE:LIB logs are retained. No production tree/output mutation and no claimed executable success.

Compile warnings retained: x64 balanced STLport C4103 include warnings plus pre-existing GetVersionEx deprecation; Win32 GetVersionEx deprecation. No compiler source repair was required. Source-build integration and consumer/provider ABI/runtime acceptance are separate next work.

Adding the genuine committed LCD provider path in a separate private relink removes exactly the10 LCD unresolved symbols. Release remains75 unique unresolved:60 Miles,13 libxml2,2 PCRE. See vivox-lcd-link-v1/remaining-symbols.json; this is not an inventory of dynamically loaded runtime SDKs. Debug still stops at the first x86 capture archive.
