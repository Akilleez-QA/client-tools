@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cl /nologo /EHsc /MT /O2 /IC:\vendor-miles-probe C:\vendor-miles-probe\miles-command-host.cpp /FoC:\vendor-miles-probe\miles-command-host.obj /FeC:\vendor-miles-probe\miles-command-host.exe winmm.lib user32.lib
if errorlevel 1 exit /b %errorlevel%
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
cl /nologo /EHsc /MT /O2 C:\vendor-miles-probe\miles-controller.cpp /FoC:\vendor-miles-probe\miles-controller.obj /FeC:\vendor-miles-probe\miles-controller.exe
exit /b %errorlevel%
