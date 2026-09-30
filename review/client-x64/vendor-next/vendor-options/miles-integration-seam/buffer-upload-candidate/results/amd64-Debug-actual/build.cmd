@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul
if errorlevel 1 exit /b 1
cd /d "C:\miles-upload-parent17-v2\amd64-Debug-actual"
cl /nologo /EHsc /W4 /WX /MTd /Od "C:\miles-upload-parent17-v2\buffer-upload-candidate\buffer_upload.cpp" "C:\miles-upload-parent17-v2\buffer-upload-candidate\tests.cpp" /Fe"C:\miles-upload-parent17-v2\amd64-Debug-actual\test.exe"
exit /b %errorlevel%
