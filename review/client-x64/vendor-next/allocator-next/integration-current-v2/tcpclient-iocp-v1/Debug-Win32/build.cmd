@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul
cl /nologo /EHsc /MTd /Od /I"C:/integration-current-v1/workspace/repo/src/external/3rd/library/miles/include" C:/tcpclient-iocp-probe.cpp /Fo"C:\tcpclient-iocp-v1\Debug-Win32\probe.obj" /Fe"C:\tcpclient-iocp-v1\Debug-Win32\probe.exe"
exit /b %errorlevel%
