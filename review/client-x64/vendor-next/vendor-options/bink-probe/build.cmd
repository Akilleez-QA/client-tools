@echo off
cd /d C:\vendor-bink-probe
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86
cl /nologo /EHsc /MT /W4 /I. probe.cpp /Fe:probe32.exe /link /MACHINE:X86
if errorlevel 1 exit /b 1
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64
cl /nologo /EHsc /MT /W4 driver.cpp /Fe:driver64.exe /link /MACHINE:X64
