from pathlib import Path
import subprocess,json,re,hashlib
out=Path('C:/integrated-wrapper-link-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','R:','C:/integration-current-v2/workspace'],check=True);root=Path('R:/repo');project=root/'src/game/client/application/SwgClient/build/win32';rows=[]
for cfg,suffix in [('Release','r'),('Debug','d')]:
 d=out/cfg;d.mkdir();lines=Path('C:/integration-incremental-v3/results',cfg+'.log').read_text(errors='replace').splitlines();matches=[i for i,l in enumerate(lines) if 'link.exe /ERRORREPORT:QUEUE /OUT:' in l and 'SwgClient_'+suffix+'.exe' in l];assert len(matches)==1
 i=matches[0];command=lines[i].strip();exe,command=command.split('link.exe ',1);link=exe+'link.exe';i+=1
 while i<len(lines) and lines[i].strip().startswith('"'):
  command+='\n'+lines[i].strip();i+=1
 (d/'original.rsp').write_text(command)
 assert command.count(' stlport_vc71_stldebug_static.lib ')==1
 command=command.replace(' stlport_vc71_stldebug_static.lib ',' ')
 for flag,name in [('OUT','SwgClient.exe'),('PDB','SwgClient.pdb'),('IMPLIB','SwgClient.lib')]:
  command,n=re.subn('/'+flag+':"[^"]+"','/'+flag+':"'+str(d/name).replace('\\','/')+'"',command,flags=re.I);assert n==1,(flag,n)
 provider=Path('C:/vivox-props-target-v1')/cfg/'deps/stlport.lib';assert provider.is_file()
 command='"'+str(provider)+'" '+command+'\n/NODEFAULTLIB:stlport_vc71_static.lib /VERBOSE:LIB /MAP:"'+str(d/'SwgClient.map')+'"'
 wrapper=Path('C:/vivox-props-target-v1')/cfg/'deps/vivoxSharedWrapper.lib'
 command,n=re.subn(r'(?i)(?<!\S)vivoxSharedWrapper_(?:Release|Debug)\.lib(?!\S)', '',command);assert n>=1
 command='"'+str(wrapper)+'" '+command
 (d/'wrapper.json').write_text(json.dumps(dict(path=str(wrapper),sha256=hashlib.sha256(wrapper.read_bytes()).hexdigest(),removed_explicit_entries=n),indent=2))
 command='/LIBPATH:"C:/lcd-props-eval-v1/LCDSDK/Lib/x64" '+command
 pcre=Path('C:/pcre-native-v3')/('amd64-'+cfg)/'pcre-4.1/pcre.lib'
 xml=Path('C:/xml-pcre-next-v3')/('amd64-'+cfg)/'libxml2-2.6.7/win32/bin.msvc/libxml2.lib'
 command,np=re.subn(r'(?i)(?<!\S)libpcre\.a(?!\S)', '',command);assert np>=1
 command,nx=re.subn(r'(?i)(?<!\S)"?libxml2-win32-(?:release|debug)\.lib"?(?!\S)', '',command);assert nx>=1
 command='"'+str(pcre)+'" "'+str(xml)+'" '+command
 (d/'xml-pcre.json').write_text(json.dumps(dict(pcre=dict(path=str(pcre),sha256=hashlib.sha256(pcre.read_bytes()).hexdigest(),removed=np),xml=dict(path=str(xml),sha256=hashlib.sha256(xml.read_bytes()).hexdigest(),removed=nx)),indent=2))
 rsp=d/'candidate.rsp';rsp.write_text(command)
 batch=d/'link.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\n"'+link+'" @"'+str(rsp)+'"\n')
 r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'link.log').write_bytes(r.stdout)
 row=dict(configuration=cfg,exit=r.returncode,provider=str(provider),provider_sha256=hashlib.sha256(provider.read_bytes()).hexdigest());rows.append(row);print(row,flush=True)
(out/'results.json').write_text(json.dumps(rows,indent=2))
