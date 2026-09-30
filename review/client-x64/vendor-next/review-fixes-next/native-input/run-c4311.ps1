$ErrorActionPreference='Continue'
Set-Location 'C:\review-fixes-next-0d2f8c168'
foreach ($v in @('before','after')) {
 @('@echo off','call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64 >nul',('cl /nologo /c /W4 /w14311 /WX /Fo'+$v+'-4311.obj '+$v+'.cpp'),'exit /b %errorlevel%') | Set-Content "$v-4311.cmd" -Encoding ASCII
 cmd /d /c "$v-4311.cmd" *> "$v-4311.log"
 "$v explicit-C4311 $LASTEXITCODE" | Add-Content status-4311.txt
}
Get-Content status-4311.txt
