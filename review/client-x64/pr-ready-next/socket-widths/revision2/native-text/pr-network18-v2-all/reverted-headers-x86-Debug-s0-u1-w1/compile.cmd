@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b %errorlevel%
cl /nologo /EHsc /W4 /Zc:wchar_t- /GR /Gy /showIncludes /MTd /Od /D_DEBUG /DWIN32 /DSOCKET_PROBE_SOCK=0 /DSOCKET_PROBE_UDP=1 /DSOCKET_PROBE_WINSOCK_FIRST=1 /IC:\pr-network18-v2-all\reverted-headers\src /IC:\pr-network18-v2-source\src /IC:\pr-network18-v2-source\src\engine\shared\library\sharedNetwork\include\public /IC:\pr-network18-v2-source\src\external\3rd\library\soePlatform\VChatAPI\utils2.0\utils /IC:\pr-network18-v2-source\src\external\3rd\library\udplibrary C:\pr-network18-v2-source\tools\test-windows-network-widths\probe.cpp /FoC:\pr-network18-v2-all\reverted-headers-x86-Debug-s0-u1-w1\case.obj /FeC:\pr-network18-v2-all\reverted-headers-x86-Debug-s0-u1-w1\case.exe /link Ws2_32.lib
exit /b %errorlevel%
