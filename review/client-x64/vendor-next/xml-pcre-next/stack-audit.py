from pathlib import Path
import struct,json
paths=[Path('C:/client-next-build/src/compile/win32/SwgClient/Release/SwgClient_r.exe'),Path('C:/client-next-build/src/compile/win32/SwgClient/Debug/SwgClient_d.exe')]+list(Path('C:/pcre-corpus-v2').glob('*/pcretest.exe'))
out=[]
for p in paths:
 if not p.exists():out.append(dict(path=str(p),exists=False));continue
 b=p.read_bytes();pe=struct.unpack_from('<I',b,0x3c)[0];opt=pe+24;magic=struct.unpack_from('<H',b,opt)[0];reserve,commit=struct.unpack_from('<QQ' if magic==0x20b else '<II',b,opt+72);out.append(dict(path=str(p),exists=True,stack_reserve=reserve,stack_commit=commit))
Path('C:/pcre-corpus-v2/stack-audit.json').write_text(json.dumps(out,indent=2))
