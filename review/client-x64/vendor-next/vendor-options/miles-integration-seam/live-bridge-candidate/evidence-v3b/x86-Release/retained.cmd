@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
cd /d "C:\miles-live-bridge-v3b\x86-Release"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /I"C:\miles-live-bridge-v3b\host-candidate" /MT /O2 "C:\miles-live-bridge-v3b\host-candidate\retained_buffers_test.cpp" "C:\miles-live-bridge-v3b\host-candidate\retained_buffers.cpp" /Fe"C:\miles-live-bridge-v3b\x86-Release\retained.exe"
