@echo off
cd /d C:\miles-cadence-20260930-a
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cl /nologo /EHsc /MT /O2 /W4 probe.cpp /Foprobe.obj /Feprobe.exe
exit /b %errorlevel%
