@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-imemmove18-v1\tools\run.py --checkout C:\pr-imemmove18-v1\baseline --out C:\pr-imemmove18-v1\results\baseline-64-Debug --bits 64 --configuration Debug --baseline --expect-ambiguity
exit /b %errorlevel%
