@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cd /d C:\vendor-vivox-probe
cl /nologo /EHsc /MT /O2 /Iinclude probe.cpp /Feprobe32.exe > build32.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe32.exe > run32.log 2>&1
echo %errorlevel% > exit32.txt
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
cl /nologo /EHsc /MT /O2 /Iinclude probe.cpp /Feprobe64.exe > build64.log 2>&1
if errorlevel 1 exit /b %errorlevel%
probe64.exe > run64.log 2>&1
echo %errorlevel% > exit64.txt
