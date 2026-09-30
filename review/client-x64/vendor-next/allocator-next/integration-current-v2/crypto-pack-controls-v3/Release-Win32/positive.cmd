@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
cl /nologo /EHsc /W3 /MT /O2 /DNDEBUG /D_CRT_SECURE_NO_DEPRECATE=1 /I"C:\integration-current-v1\workspace\repo\src\external\3rd\library\stlport453\stlport" /I"C:\integration-current-v1\workspace\repo\src\external\ours\library\crypto\src\shared\core" /I"C:\integration-current-v1\workspace\repo\src\external\ours\library\crypto\src\shared\original" /WX /c "C:\crypto-pack-controls-v3\Release-Win32\positive.cpp" /Fo"C:\crypto-pack-controls-v3\Release-Win32\positive.obj"
exit /b %errorlevel%
