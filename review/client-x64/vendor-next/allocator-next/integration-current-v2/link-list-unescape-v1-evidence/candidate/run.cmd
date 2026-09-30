@echo off
call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul
"C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe" "C:\link-list-unescape-v1\candidate\repo\src\game\client\application\SwgClient\build\win32\SwgClient.vcxproj" /t:Audit /p:Configuration=Release /p:Platform=x64 /p:SwgSourceRoot=R:/repo/src/ /p:DXSDK_DIR=C:/SDKs/DXSDK /p:SwgLogitechLcdSdkDir=C:/lcd-props-eval-v1/LCDSDK /p:ForceImportAfterCppTargets="C:\link-list-unescape-v1\candidate\audit.targets" /v:normal /nologo
