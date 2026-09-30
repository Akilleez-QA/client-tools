@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b 1
cd /d "C:\miles-live-bridge-mutation-v1\x86-Release"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /IC:/client-next-build/src/external/3rd/library/miles/include /MT /O2 "C:\miles-live-bridge-mutation-v1\live-bridge-candidate\bridge.cpp" "C:\miles-live-bridge-mutation-v1\transport-candidate\codec.cpp" "C:\miles-live-bridge-mutation-v1\pipe-transport-candidate\endpoint.cpp" "C:\miles-live-bridge-mutation-v1\coordinator-candidate\coordinator.cpp" "C:\miles-live-bridge-mutation-v1\host-candidate\host_dispatch.cpp" "C:\miles-live-bridge-mutation-v1\host-candidate\retained_buffers.cpp" "C:\miles-live-bridge-mutation-v1\buffer-upload-candidate\buffer_upload.cpp" C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib /Fe"C:\miles-live-bridge-mutation-v1\x86-Release\host.exe"
