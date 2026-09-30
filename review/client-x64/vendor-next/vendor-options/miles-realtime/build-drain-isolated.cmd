@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cl /nologo /EHsc /MT /O2 /IC:\vendor-miles-probe C:\vendor-miles-probe\probe-drain-isolated.cpp /FoC:\vendor-miles-probe\probe-drain-isolated.obj /FeC:\vendor-miles-probe\probe-drain-isolated.exe winmm.lib user32.lib
exit /b %errorlevel%
