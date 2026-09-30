@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b 1
cl /nologo /EHsc /DWIN32 /MTd /Od /IC:/client-next-build/src/external/3rd/library/miles/include C:\miles-preflight-parent15\host-candidate\host_dispatch.cpp C:\miles-preflight-parent15\host-candidate\preflight.cpp C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib delayimp.lib /FeC:\miles-preflight-parent15\Debug-actual\probe.exe /link /DELAYLOAD:mss32.dll
exit /b %errorlevel%
