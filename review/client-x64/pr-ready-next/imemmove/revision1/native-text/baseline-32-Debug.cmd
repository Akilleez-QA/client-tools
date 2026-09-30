@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-imemmove18-v1\tools\run.py --checkout C:\pr-imemmove18-v1\baseline --out C:\pr-imemmove18-v1\results\baseline-32-Debug --bits 32 --configuration Debug --baseline
exit /b %errorlevel%
