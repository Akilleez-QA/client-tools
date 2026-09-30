@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b 1
cd /d "C:\miles-live-bridge-v3\x86-Debug"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /IC:/client-next-build/src/external/3rd/library/miles/include /MTd /Od "C:\miles-live-bridge-v3\live-bridge-candidate\bridge.cpp" "C:\miles-live-bridge-v3\transport-candidate\codec.cpp" "C:\miles-live-bridge-v3\pipe-transport-candidate\endpoint.cpp" "C:\miles-live-bridge-v3\coordinator-candidate\coordinator.cpp" "C:\miles-live-bridge-v3\host-candidate\host_dispatch.cpp" "C:\miles-live-bridge-v3\host-candidate\retained_buffers.cpp" "C:\miles-live-bridge-v3\buffer-upload-candidate\buffer_upload.cpp" C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib /Fe"C:\miles-live-bridge-v3\x86-Debug\host.exe"
