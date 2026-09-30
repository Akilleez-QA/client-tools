@echo off
set VSLANG=1033
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b 1
set
