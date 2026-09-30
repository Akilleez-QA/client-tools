@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
cl /nologo /EHsc /MT /O2 /W4 /DHOST probe.cpp /Fehost.exe
if errorlevel 1 exit /b %errorlevel%
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64
cl /nologo /EHsc /MT /O2 /W4 probe.cpp /Fecontroller.exe
exit /b %errorlevel%
