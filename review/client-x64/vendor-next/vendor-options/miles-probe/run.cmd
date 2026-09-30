@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cd /d C:\vendor-miles-probe
cl /nologo /EHsc /MT /O2 probe.cpp /Feprobe.exe winmm.lib user32.lib > compile.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe.exe C:\vendor-miles-probe\Mss32.dll C:\vendor-miles-probe\sample.wav > run.log 2>&1
exit /b %errorlevel%
