@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
cl @"C:\pr-imemmove18-v1\caller-results-v2\win32-Release-sharedFile\compile.rsp"
