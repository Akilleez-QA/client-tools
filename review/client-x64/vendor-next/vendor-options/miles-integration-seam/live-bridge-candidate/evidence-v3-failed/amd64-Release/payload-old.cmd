@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
cd /d "C:\miles-live-bridge-v3\amd64-Release"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /I"C:\miles-live-bridge-v3\host-candidate" /MT /O2 "C:\miles-live-bridge-v3\live-bridge-candidate\payload-allocation-test.cpp" "C:\miles-live-bridge-v3\live-bridge-candidate\retained-v2-control.cpp" /Fe"C:\miles-live-bridge-v3\amd64-Release\payload-old.exe"
