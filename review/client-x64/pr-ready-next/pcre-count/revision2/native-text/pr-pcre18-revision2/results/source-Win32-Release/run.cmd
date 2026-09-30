@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-pcre18-revision2\tools\test-pcre-capture-count\run.py --checkout C:\pr-pcre18-revision2 --include-dir C:\pcre-native-v3\x86-Release\pcre-4.1 --library C:\parser-integration-v3\Win32-Release\pcre.lib --bits 32 --configuration Release --out C:\pr-pcre18-revision2\results\source-Win32-Release
exit /b %errorlevel%
