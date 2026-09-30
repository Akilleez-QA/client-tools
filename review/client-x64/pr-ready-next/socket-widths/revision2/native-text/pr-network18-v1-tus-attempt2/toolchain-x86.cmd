@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b %errorlevel%
where cl
where link
cl /Bv
set INCLUDE
set LIB
ver
