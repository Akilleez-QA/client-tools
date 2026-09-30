@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-pcre18-revision2\tools\test-pcre-capture-count\run.py --checkout C:\pr-pcre18-revision2 --include-dir C:\pr-pcre18-revision2\original-header --library C:\xml-pcre-next\legacy-libpcre.a --bits 32 --configuration Debug --out C:\pr-pcre18-revision2\results-final\original-Win32-Debug
exit /b %errorlevel%
