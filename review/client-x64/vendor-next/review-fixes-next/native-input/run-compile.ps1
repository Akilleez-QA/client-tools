$ErrorActionPreference = 'Continue'
Set-Location 'C:\review-fixes-next-0d2f8c168'
foreach ($arch in @('x86','amd64')) {
 foreach ($v in @('before','after')) {
  $lines = @('@echo off', ('call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" '+$arch+' >nul'), ('cl /nologo /c /W4 /WX /Fo'+$v+'-'+$arch+'.obj '+$v+'.cpp'), 'exit /b %errorlevel%')
  $lines | Set-Content "$v-$arch.cmd" -Encoding ASCII
  cmd /d /c "$v-$arch.cmd" *> "$v-$arch.compile.log"
  "$v $arch compile $LASTEXITCODE" | Add-Content status.txt
 }
}
foreach ($define in @('DEBUG','NDEBUG','_DEBUG')) {
 @('@echo off','call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86 >nul',"cl /nologo /P /D$define /Figuard-$define.i guard.cpp",'exit /b %errorlevel%') | Set-Content "guard-$define.cmd" -Encoding ASCII
 cmd /d /c "guard-$define.cmd" *> "guard-$define.log"
 "guard $define $LASTEXITCODE" | Add-Content status.txt
}
Get-Content status.txt
