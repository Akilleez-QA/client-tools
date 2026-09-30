@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-pcre18-revision2\tools\test-pcre-capture-count\run.py --checkout C:\pr-pcre18-revision2 --include-dir C:\pcre-native-v3\x86-Debug\pcre-4.1 --library C:\parser-integration-v3\Win32-Debug\pcre.lib --bits 32 --configuration Debug --out C:\pr-pcre18-revision2\results-final\source-Win32-Debug
exit /b %errorlevel%
