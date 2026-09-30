from pathlib import Path
import struct,zlib,json,collections
root=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0');rows=[];errors=[]
for p in root.glob('*.tre'):
 try:
  with p.open('rb') as f:
   h=struct.unpack('<9I',f.read(36));n,off,tc,ts,nc,ns,nu=h[2:];f.seek(off);t=f.read(ts if tc else n*24);t=zlib.decompress(t) if tc else t;names=f.read(ns if nc else nu);names=zlib.decompress(names) if nc else names
   assert len(t)==n*24 and len(names)==nu
   for i in range(n):
    crc,size,pos,comp,packed,no=struct.unpack_from('<6I',t,i*24);name=names[no:names.index(b'\0',no)].decode();ext=Path(name).suffix.lower()
    if ext in ('.wav','.mp3','.ogg','.bik','.flac','.aiff'):rows.append(dict(tre=str(p),name=name,size=size,offset=pos,compression=comp,packed=packed))
 except Exception as e:errors.append([str(p),str(e)])
Path('/home/akilleez/Work/client-wire-validation/vendor-options/tre-media-inventory.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));print(collections.Counter(Path(x['name']).suffix for x in rows));print('errors',errors[:3]);print('bik',sorted([r for r in rows if r['name'].endswith('.bik')],key=lambda x:x['size'])[:2])
