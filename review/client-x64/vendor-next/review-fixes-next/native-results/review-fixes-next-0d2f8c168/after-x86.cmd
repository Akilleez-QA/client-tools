@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cl /nologo /c /W4 /WX /Foafter-x86.obj after.cpp
exit /b %errorlevel%
