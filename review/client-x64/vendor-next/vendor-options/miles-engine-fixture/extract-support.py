from pathlib import Path
import struct,zlib,json,hashlib
root=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0');out=Path(__file__).resolve().parent/'private-support';out.mkdir(exist_ok=True);rows=[]
want={'datatables/manifest/skufree.iff','datatables/music/music.iff'}
for p in root.glob('*.tre'):
 with p.open('rb') as f:
  h=struct.unpack('<9I',f.read(36));n,off,tc,ts,nc,ns,nu=h[2:];f.seek(off);t=f.read(ts if tc else n*24);t=zlib.decompress(t) if tc else t;names=f.read(ns if nc else nu);names=zlib.decompress(names) if nc else names
  for i in range(n):
   crc,size,pos,comp,packed,no=struct.unpack_from('<6I',t,i*24);name=names[no:names.index(b'\0',no)].decode()
   if name in want:
    f.seek(pos);data=f.read(packed if comp else size);data=zlib.decompress(data) if comp else data;assert len(data)==size
    target=out/p.stem/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);rows.append(dict(tre=p.name,path=name,size=size,sha256=hashlib.sha256(data).hexdigest(),extracted=str(target)))
(Path(__file__).parent/'support-assets.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
