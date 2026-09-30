@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul
if errorlevel 1 exit /b %errorlevel%
"C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe" "Q:\repo\src\game\client\application\SwgClient\build\win32\SwgClient.vcxproj" /t:StrictRelink /p:Configuration=Debug /p:Platform=x64 /p:ForceImportAfterCppTargets="C:\strict-link-policy-v2\candidate\check.targets" /v:normal /nologo
