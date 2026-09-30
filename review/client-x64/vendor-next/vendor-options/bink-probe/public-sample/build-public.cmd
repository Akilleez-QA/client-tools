@echo off
cd /d C:\vendor-bink-probe
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86
cl /nologo /EHsc /MT /W4 /I. public-sample\probe-public.cpp /Fo:public-sample\ /Fe:public-sample\probe-public32.exe /link /MACHINE:X86
if errorlevel 1 exit /b 1
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64
cl /nologo /EHsc /MT /W4 public-sample\driver-public.cpp /Fo:public-sample\ /Fe:public-sample\driver-public64.exe /link /MACHINE:X64
