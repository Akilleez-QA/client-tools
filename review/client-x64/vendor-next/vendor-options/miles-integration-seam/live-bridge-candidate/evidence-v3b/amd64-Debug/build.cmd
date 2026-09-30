@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b 1
cd /d "C:\miles-live-bridge-v3b\amd64-Debug"
cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /IC:/client-next-build/src/external/3rd/library/miles/include /MTd /Od "C:\miles-live-bridge-v3b\live-bridge-candidate\bridge.cpp" "C:\miles-live-bridge-v3b\transport-candidate\codec.cpp" "C:\miles-live-bridge-v3b\pipe-transport-candidate\endpoint.cpp" "C:\miles-live-bridge-v3b\coordinator-candidate\coordinator.cpp" /Fe"C:\miles-live-bridge-v3b\amd64-Debug\controller.exe"
