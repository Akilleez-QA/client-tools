@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cd /d C:\vendor-vivox-probe
cl /nologo /EHsc /MT /O2 /Iinclude probe-v2.cpp /Feprobe32-v2.exe > build32-v2.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe32-v2.exe > run32-v2.log 2>&1
echo %errorlevel% > exit32-v2.txt
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
cl /nologo /EHsc /MT /O2 /Iinclude probe-v2.cpp /Feprobe64-v2.exe > build64-v2.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe64-v2.exe > run64-v2.log 2>&1
echo %errorlevel% > exit64-v2.txt
