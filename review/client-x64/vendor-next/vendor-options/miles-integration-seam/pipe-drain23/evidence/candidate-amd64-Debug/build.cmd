@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b 1
cl /nologo /EHsc /W4 /WX /D_WIN32_WINNT=0x0601 /MTd /Od /DDRAIN23_CANDIDATE  /I"C:\pipe-drain23\candidate" "C:\pipe-drain23\endpoint-under-test.cpp" "C:\pipe-drain23\drain-fixture.cpp" "C:\pipe-drain23\candidate\transport-candidate\codec.cpp" /Fe"C:\pipe-drain23\candidate-amd64-Debug\fixture.exe"
