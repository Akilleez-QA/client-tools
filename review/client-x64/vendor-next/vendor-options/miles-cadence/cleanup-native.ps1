$ErrorActionPreference='Stop'
$p='C:\miles-cadence-20260930-a'
Get-FileHash "$p\probe.exe", "$p\probe.cpp", "$p\Mss.h", 'C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\cl.exe' -Algorithm SHA256 | Format-List
Remove-Item -LiteralPath $p -Recurse -Force
"scratch_exists=$(Test-Path $p)"
