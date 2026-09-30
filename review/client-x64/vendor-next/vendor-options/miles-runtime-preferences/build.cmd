@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b %errorlevel%
cl /nologo /EHsc /MT /O2 /W4 /WX /DWIN32 /IC:/client-next-build/src/external/3rd/library/miles/include probe.cpp /Feprobe.exe
exit /b %errorlevel%
