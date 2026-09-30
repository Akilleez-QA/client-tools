import pathlib,struct,zlib,json,hashlib
base=pathlib.Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0'); out=pathlib.Path(__file__).parent
budget=256*1024**2
candidates=[]; errors=[]; scanned=[]
def block(f,off,size,codec,expected):
 global budget
 assert 0<=size<=32*1024**2 and 0<=expected<=32*1024**2 and codec in (0,2)
 assert off>=36 and off+size<=f.seek(0,2)
 budget-=size; assert budget>=0
 f.seek(off); b=f.read(size)
 if codec==2:
  d=zlib.decompressobj(); b=d.decompress(b,expected+1); assert d.eof and not d.unconsumed_tail
 assert len(b)==expected
 return b
for p in sorted(base.glob('*.tre'))[:256]:
 try:
  with p.open('rb') as f:
   scanned.append(p.name)
   h=f.read(36); tag,ver,n,off,tc,ts,nc,ns,nu=struct.unpack('<4s4s7I',h)
   assert tag==b'EERT' and ver in (b'4000',b'5000'), ('unsupported_header',tag.hex(),ver.decode('ascii','replace'),n)
   toc=block(f,off,ts if tc else n*24,tc,n*24)
   names=block(f,off+(ts if tc else n*24),ns if nc else nu,nc,nu)
   for i in range(n):
    crc,length,pos,codec,packed,no=struct.unpack_from('<I5i',toc,i*24)
    assert 0<=no<len(names)
    end=names.find(b'\0',no); assert end>=no
    name=names[no:end].decode('utf8')
    if name.lower().endswith('.bik') and 0<length<=64*1024**2:
     candidates.append(dict(tre=str(p),name=name,size=length,offset=pos,codec=codec,packed=packed))
 except Exception as e: errors.append(dict(tre=p.name,error=repr(e)))
(out/'asset.json').write_text(json.dumps(dict(candidates=candidates,errors=errors,scanned=scanned,metadata_read_bytes=256*1024**2-budget),indent=2))
if not candidates:
 print('No bounded .bik candidates found'); raise SystemExit(0)
candidates.sort(key=lambda x:(x['size'],x['tre'],x['name'])); selected=candidates[0]
with open(selected['tre'],'rb') as f:
 size=selected['packed'] if selected['codec'] else selected['size']
 assert selected['codec'] in (0,2) and 0<size<=64*1024**2
 assert 36<=selected['offset']<=f.seek(0,2)-size
 f.seek(selected['offset']); b=f.read(size)
 if selected['codec']==2:
  d=zlib.decompressobj(); b=d.decompress(b,selected['size']+1); assert d.eof and not d.unconsumed_tail
 assert len(b)==selected['size']
(out/'private/movie.bik').write_bytes(b)
selected['sha256']=hashlib.sha256(b).hexdigest(); selected['header_hex']=b[:44].hex()
(out/'asset.json').write_text(json.dumps(dict(selected=selected,candidates=candidates,errors=errors,metadata_read_bytes=256*1024**2-budget),indent=2))
print(json.dumps(selected,indent=2))
