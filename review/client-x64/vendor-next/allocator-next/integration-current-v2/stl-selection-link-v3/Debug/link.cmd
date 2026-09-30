@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul
if errorlevel 1 exit /b %errorlevel%
"C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\x86_amd64\link.exe" @"C:\stl-selection-link-v3\Debug\candidate.rsp"
