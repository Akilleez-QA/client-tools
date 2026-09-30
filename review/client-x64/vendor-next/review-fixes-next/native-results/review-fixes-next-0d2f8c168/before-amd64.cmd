@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
cl /nologo /c /W4 /WX /Fobefore-amd64.obj before.cpp
exit /b %errorlevel%
