@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b %errorlevel%
cl /nologo /EHsc /MT /O2 /W4 /WX /D_CRT_SECURE_NO_WARNINGS "C:\trackir-registry-boundary-20261001T101053Z-7e4ddf57\probe.cpp" /Fo"C:\trackir-registry-boundary-20261001T101053Z-7e4ddf57\x64\probe.obj" /Fe"C:\trackir-registry-boundary-20261001T101053Z-7e4ddf57\x64\probe.exe" /link advapi32.lib
exit /b %errorlevel%
