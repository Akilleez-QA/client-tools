@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
cl /nologo /EHsc /W3 /MT /O2 /DNDEBUG /D_CRT_SECURE_NO_DEPRECATE=1 /I"C:\integration-current-v1\workspace\repo\src\external\3rd\library\stlport453\stlport" /I"C:\integration-current-v1\workspace\repo\src\external\ours\library\crypto\src\shared\core" /I"C:\integration-current-v1\workspace\repo\src\external\ours\library\crypto\src\shared\original" C:/crypto-pack-candidate.cpp /Fo"C:\crypto-pack-after-v3\Release-Win32\probe.obj" /Fe"C:\crypto-pack-after-v3\Release-Win32\probe.exe" /link /NODEFAULTLIB:stlport_vc71_static.lib /NODEFAULTLIB:stlport_vc71_stldebug_static.lib "C:/client-next-build/src/external/3rd/library/stlport453/lib/win32/stlport_vc71_static.lib"
exit /b %errorlevel%
