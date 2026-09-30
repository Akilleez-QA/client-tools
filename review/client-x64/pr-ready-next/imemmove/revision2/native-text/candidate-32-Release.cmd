@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86
if errorlevel 1 exit /b 1
C:/ci-dpvs-review/python/python.exe C:\pr-imemmove18-v2\tools\run.py --checkout C:\pr-imemmove18-v2\candidate --out C:\pr-imemmove18-v2\results\candidate-32-Release --bits 32 --configuration Release
exit /b %errorlevel%
