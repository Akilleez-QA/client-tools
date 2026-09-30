@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul
if errorlevel 1 exit /b %errorlevel%
cl /nologo /EHsc /W4 /Zc:wchar_t- /GR /Gy /showIncludes /MT /O2 /DNDEBUG /DWIN32 /DSOCKET_PROBE_SOCK=1 /DSOCKET_PROBE_UDP=2 /DSOCKET_PROBE_WINSOCK_FIRST=0 /IC:\pr-network18-v2-all\reverted-headers\src /IC:\pr-network18-v2-source\src /IC:\pr-network18-v2-source\src\engine\shared\library\sharedNetwork\include\public /IC:\pr-network18-v2-source\src\external\3rd\library\soePlatform\VChatAPI\utils2.0\utils /IC:\pr-network18-v2-source\src\external\3rd\library\soePlatform\VChatAPI\utils2.0\utils\UdpLibrary C:\pr-network18-v2-source\tools\test-windows-network-widths\probe.cpp /FoC:\pr-network18-v2-all\reverted-headers-x86-Release-s1-u2-w0\case.obj /FeC:\pr-network18-v2-all\reverted-headers-x86-Release-s1-u2-w0\case.exe /link Ws2_32.lib
exit /b %errorlevel%
