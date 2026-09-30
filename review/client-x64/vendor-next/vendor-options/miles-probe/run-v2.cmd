@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cd /d C:\vendor-miles-probe
cl /nologo /EHsc /MT /O2 probe-v2.cpp /Feprobe.exe winmm.lib user32.lib > compile-v2.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe.exe C:\vendor-miles-probe\Mss32.dll C:\vendor-miles-probe\sample.wav C:\vendor-miles-probe\sample.mp3 > run-v2.log 2>&1
exit /b %errorlevel%
