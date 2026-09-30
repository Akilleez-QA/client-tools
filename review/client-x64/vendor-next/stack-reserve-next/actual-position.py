from pathlib import Path
import subprocess,tarfile,json,struct
root=Path('C:/stack-actual-position-v1');root.mkdir(exist_ok=True)
with tarfile.open('C:/stack-position-input.tar') as t:t.extractall(root)
target=root/'audit.targets';target.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><Link Include="__metadata_only"/></ItemGroup><Target Name="StackMetadata"><Message Importance="High" Text="STACK|$(ProjectName)|$(Platform)|$(Configuration)|%(Link.StackReserveSize)|%(Link.StackCommitSize)"/></Target></Project>')
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';rows=[]
for variant in ['baseline','candidate']:
 for platform,arch in [('Win32','x86'),('x64','amd64')]:
  for cfg in ['Debug','Release']:
   out=root/(variant+'-'+platform+'-'+cfg);out.mkdir(exist_ok=True)
   project=root/variant/'src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj'
   cmd=[ms,str(project),'/t:StackMetadata','/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(target),'/p:DXSDK_DIR=C:/SDKs/DXSDK','/nologo','/v:minimal'];r=subprocess.run(cmd,capture_output=True);(out/'evaluation.log').write_bytes(r.stdout+r.stderr)
   lines=[s.strip() for s in r.stdout.decode('cp1252').splitlines() if 'STACK|' in s];entry=dict(variant=variant,platform=platform,cfg=cfg,evaluation_exit=r.returncode,metadata=lines);rows.append(entry)
   if r.returncode or len(lines)!=1:continue
   fields=lines[0].split('|');reserve,commit=fields[-2:]
   source=out/'proxy.c';source.write_text('int main(void) { return 0; }\n')
   stack=('/STACK:'+reserve+((','+commit) if commit else '')) if reserve else ''
   batch=out/'build.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\ncl /nologo '+('/MTd' if cfg=='Debug' else '/MT')+' proxy.c /Feproxy.exe /link '+stack+'\n')
   r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=out,capture_output=True);(out/'proxy-build.log').write_bytes(r.stdout+r.stderr);entry['proxy_build_exit']=r.returncode
   if not r.returncode:
    b=(out/'proxy.exe').read_bytes();pe=struct.unpack_from('<I',b,0x3c)[0];opt=pe+24;magic=struct.unpack_from('<H',b,opt)[0];fmt='<QQ' if magic==0x20b else '<II';entry['proxy_stack_reserve'],entry['proxy_stack_commit']=struct.unpack_from(fmt,b,opt+72)
(root/'results.json').write_text(json.dumps(rows,indent=2))
