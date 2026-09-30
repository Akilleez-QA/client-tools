@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
cd /d "C:\miles-live-bridge-v3\amd64-Debug"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /I"C:\miles-live-bridge-v3\host-candidate" /MTd /Od "C:\miles-live-bridge-v3\host-candidate\retained_buffers_test.cpp" "C:\miles-live-bridge-v3\host-candidate\retained_buffers.cpp" /Fe"C:\miles-live-bridge-v3\amd64-Debug\retained.exe"
