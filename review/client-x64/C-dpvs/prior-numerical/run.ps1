param([string]$Root='C:\swg-x64-b5bb8792\dpvs-headers-probe')
$ErrorActionPreference='Stop'
Set-Location $Root
# Place this complete x87 directory under Root; use existing candidate include/interface and obj-ARCH.
$runId=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
foreach($case in @(@('x86','native'),@('x86','scalar'),@('amd64','native'))) {
 $arch=$case[0];$kind=$case[1];if($arch -ne 'amd64'){continue};$out="x87\production-double-pc64\probe-$runId-$arch-$kind"
 New-Item -ItemType Directory $out | Out-Null
 $defs='';if($kind -eq 'scalar'){$defs='/DPROBE_SCALAR_MATH'}
 $sourceNames=(Get-ChildItem sources\*.cpp).BaseName
 $objects=Get-ChildItem "obj-$arch\*.obj" | Where-Object {$_.Name -ne 'dpvsMath.obj' -and $_.BaseName -in $sourceNames}
 if($objects.Count -ne 69){throw "Expected69 non-math candidate objects, found $($objects.Count)"}
 $objects.FullName | ForEach-Object {'"'+$_+'"'} | Set-Content "$out\objects.rsp" -Encoding ASCII
 $cmd='call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" '+$arch+' >nul && cl /nologo /W4 /O2 /Ob1 /fp:precise /EHsc /MT /DWIN32 /DNDEBUG /DDPVS_DLL /DDPVS_BUILD_LIBRARY '+$defs+' /Iinclude /Iinterface /c x87\production-double-pc64\probe.cpp /Fo'+$out+'\probe.obj > '+$out+'\compile.log 2>&1 && link /nologo /OUT:'+$out+'\probe.exe '+$out+'\probe.obj @'+$out+'\objects.rsp kernel32.lib user32.lib advapi32.lib > '+$out+'\link.log 2>&1'
 cmd /c $cmd
 $buildExit=$LASTEXITCODE
 if($buildExit -ne 0){Write-Output "$out BUILD_FAILED exit=$buildExit";continue}
 & ".\$out\probe.exe" > "$out\run.log" 2>&1
 $runExit=$LASTEXITCODE
 "buildExit=$buildExit runExit=$runExit" | Set-Content "$out\status.txt"
 Write-Output "$out runExit=$runExit"
 Get-Content "$out\run.log" -Tail 1
}
foreach($case in @(@('x86','native'),@('x86','scalar'),@('amd64','native'))) {
 $arch=$case[0];$kind=$case[1];if($arch -ne 'amd64'){continue};$out="x87\production-double-pc64\caller-$runId-$arch-$kind"
 New-Item -ItemType Directory $out | Out-Null
 $defs='';if($kind -eq 'scalar'){$defs='/DPROBE_SCALAR_MATH'}
 $sourceNames=(Get-ChildItem sources\*.cpp).BaseName
 $objects=Get-ChildItem "obj-$arch\*.obj" | Where-Object {$_.Name -ne 'dpvsMath.obj' -and $_.BaseName -in $sourceNames}
 if($objects.Count -ne 69){throw "Expected69 non-math candidate objects, found $($objects.Count)"}
 $objects.FullName | ForEach-Object {'"'+$_+'"'} | Set-Content "$out\objects.rsp" -Encoding ASCII
 $cmd='call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" '+$arch+' >nul && cl /nologo /W4 /O2 /Ob1 /fp:precise /EHsc /MT /DWIN32 /DNDEBUG /DDPVS_DLL /DDPVS_BUILD_LIBRARY '+$defs+' /Iinclude /Iinterface /c x87\production-double-pc64\caller.cpp /Fo'+$out+'\probe.obj > '+$out+'\compile.log 2>&1 && link /nologo /OUT:'+$out+'\probe.exe '+$out+'\probe.obj @'+$out+'\objects.rsp kernel32.lib user32.lib advapi32.lib > '+$out+'\link.log 2>&1'
 cmd /c $cmd
 $buildExit=$LASTEXITCODE
 if($buildExit -ne 0){Write-Output "$out BUILD_FAILED exit=$buildExit";continue}
 & ".\$out\probe.exe" > "$out\run.log" 2>&1
 $runExit=$LASTEXITCODE
 "buildExit=$buildExit runExit=$runExit" | Set-Content "$out\status.txt"
 Write-Output "$out runExit=$runExit"
 Get-Content "$out\run.log" -Tail 1
}
