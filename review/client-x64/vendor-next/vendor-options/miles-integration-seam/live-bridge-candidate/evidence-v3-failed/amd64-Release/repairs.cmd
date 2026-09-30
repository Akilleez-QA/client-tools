@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
cd /d "C:\miles-live-bridge-v3\amd64-Release"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /I"C:\miles-live-bridge-v3\host-candidate" /MT /O2 "C:\miles-live-bridge-v3\live-bridge-candidate\repair-tests.cpp" "C:\miles-live-bridge-v3\transport-candidate\codec.cpp" "C:\miles-live-bridge-v3\pipe-transport-candidate\endpoint.cpp" "C:\miles-live-bridge-v3\coordinator-candidate\coordinator.cpp" /Fe"C:\miles-live-bridge-v3\amd64-Release\repairs.exe"
