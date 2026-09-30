@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
cl /nologo /P /DNDEBUG /Figuard-NDEBUG.i guard.cpp
exit /b %errorlevel%
