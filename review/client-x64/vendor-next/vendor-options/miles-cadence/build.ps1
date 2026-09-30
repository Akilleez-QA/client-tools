$ErrorActionPreference='Stop'
$p='C:\miles-cadence-20260930-a'
if(Test-Path $p){throw 'Scratch already exists'}
New-Item -ItemType Directory $p | Out-Null
