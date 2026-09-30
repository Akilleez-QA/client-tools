@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b %errorlevel%
where cl
cl @"C:\http-candidate23\results-v2\Debug-x64-stock\build.rsp"
exit /b %errorlevel%
