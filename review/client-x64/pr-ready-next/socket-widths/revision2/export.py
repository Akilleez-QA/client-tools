import hashlib,json,subprocess,sys,tarfile
from pathlib import Path
root=Path(sys.argv[1]).resolve();dest=Path(sys.argv[2]).resolve()
tracked=subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0')
paths=[]
for name in tracked:
 p=Path(name)
 if not name.startswith('src/'):continue
 if name.startswith('src/engine/shared/library/') and (p.suffix in ('.h','.hpp','.inl','.inc') or name.endswith('sharedNetwork.vcxproj') or name.endswith(('/win32/Sock.cpp','/win32/TcpClient.cpp','/win32/TcpServer.cpp'))):paths.append(name)
 elif name.startswith('src/external/ours/library/') and p.suffix in ('.h','.hpp','.inl','.inc'):paths.append(name)
 elif name.startswith('src/external/3rd/library/stlport453/stlport/'):paths.append(name)
 elif name.startswith(('src/external/3rd/library/udplibrary/','src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils/')) and p.suffix in ('.h','.hpp','.inl','.inc'):paths.append(name)
paths += ['src/engine/shared/library/sharedFoundation/src/shared/Md5.cpp','src/engine/shared/library/sharedFile/src/shared/Iff.cpp','src/engine/client/library/clientGame/src/shared/HTTPpost/TCPQueue.cpp','tools/test-windows-network-widths/run.py','tools/test-windows-network-widths/probe.cpp']
manifest={'revision':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD']).decode().strip(),'files':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
with tarfile.open(dest,'w:gz') as t:
 for p in paths:t.add(root/p,arcname=p)
dest.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(len(paths),dest.stat().st_size,manifest['revision'])
