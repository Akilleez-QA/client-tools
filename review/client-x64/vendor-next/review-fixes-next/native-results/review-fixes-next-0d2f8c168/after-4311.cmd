@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul
cl /nologo /c /W4 /w14311 /WX /Foafter-4311.obj after.cpp
exit /b %errorlevel%
