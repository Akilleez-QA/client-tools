from pathlib import Path
import subprocess,json
root=Path('C:/stack-reserve-eval-v3');root.mkdir(exist_ok=True);rows=[]
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe'
for candidate in [False,True]:
 target=root/('candidate.targets' if candidate else 'baseline.targets')
 declaration='<ItemDefinitionGroup><Link><StackReserveSize Condition="\'$(ProjectName)\'==\'SwgClient\' And \'$(Platform)\'==\'x64\'">2097152</StackReserveSize></Link></ItemDefinitionGroup>' if candidate else ''
 target.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'+declaration+'<ItemGroup><Link Include="__metadata_only"/></ItemGroup><Target Name="StackMetadata"><Message Importance="High" Text="STACK|$(ProjectName)|$(Platform)|$(Configuration)|%(Link.StackReserveSize)|%(Link.StackCommitSize)"/></Target></Project>')
 for project,path in [('SwgClient','game/client/application/SwgClient'),('Direct3d9','engine/client/application/Direct3d9')]:
  for platform in ['Win32','x64']:
   for cfg in ['Debug','Release']:
    cmd=[ms,'C:/integration-current-v2/workspace/repo/src/'+path+'/build/win32/'+project+'.vcxproj','/t:StackMetadata','/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(target),'/p:DXSDK_DIR=C:/SDKs/DXSDK','/nologo','/v:minimal']
    r=subprocess.run(cmd,capture_output=True);name=project+'-'+platform+'-'+cfg+'-'+str(candidate);(root/(name+'.log')).write_bytes(r.stdout+r.stderr)
    lines=[l.strip() for l in r.stdout.decode('cp1252').splitlines() if 'STACK|' in l];rows.append(dict(project=project,platform=platform,cfg=cfg,candidate=candidate,exit=r.returncode,metadata=lines))
(root/'results.json').write_text(json.dumps(rows,indent=2))
