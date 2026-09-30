import subprocess,pathlib,hashlib,json,struct,time
p=pathlib.Path('C:/vendor-bink-probe/public-sample'); results=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
identities=[]
for name in ['probe-public32.exe','driver-public64.exe','../binkw32.dll','logo_legal.bik']:
 b=(p/name).read_bytes(); record=dict(file=name,bytes=len(b),sha256=sha(b))
 if name.endswith(('.exe','.dll')):
  pe=struct.unpack_from('<I',b,60)[0];record['machine']=hex(struct.unpack_from('<H',b,pe+4)[0])
 identities.append(record)
assert identities[0]['machine']=='0x14c' and identities[1]['machine']=='0x8664'
assert identities[2]['sha256']=='e67e0319f9929c024a6d0757de50c65257f686f6711cb0efb7ad53afc3405dd4'
assert identities[3]['sha256']=='10c375fd8c6e2fa11db83daaabdabc94a6f9b9b77dcce52720d71b8aa2da7145'
for i in range(2):
 start=time.monotonic();r=subprocess.run([str(p/'driver-public64.exe')],capture_output=True,timeout=65,cwd=p)
 (p/('decode-%d.raw'%i)).write_bytes(r.stdout);(p/('decode-%d.stderr'%i)).write_bytes(r.stderr)
 header,payload=r.stdout.split(b'\n',1);assert header.startswith(b'BINKPUBLIC/1 ')
 fields=dict(x.split('=',1) for x in header.decode().split()[1:])
 h=14695981039346656037
 for v in payload:h=((h^v)*1099511628211)&((1<<64)-1)
 assert len(payload)==int(fields['length']) and '%016x'%h==fields['fnv1a64'] and fields['pointer_bytes']=='8' and fields['child_exit']=='0' and r.returncode==0
 events=[];frames=[];off=0
 while off<len(payload):
  end=payload.index(b'\n',off);e=json.loads(payload[off:end]);off=end+1;events.append(e)
  if e.get('kind')=='pixels':
   n=e['length'];assert n==640*480*4;buf=payload[off:off+n];off+=n
   assert payload[off:off+1]==b'\n';off+=1
   nonblack=sum(any(buf[j:j+3]) for j in range(0,len(buf),4))
   frames.append(dict(frame=e['frame'],bytes=n,sha256=sha(buf),nonblack_pixels=nonblack,alpha_values=sorted(set(buf[3::4]))))
   if i==0:(p/('frame-%02d.bgra'%e['frame'])).write_bytes(buf)
 assert events[0]['pointer_bytes']==4
 assert events[1]==dict(width=640,height=480,frames=150,rate=30,rate_div=1,tracks=0)
 assert [e['frame'] for e in events if 'decode_status' in e]==list(range(1,33))
 assert all(e['read_error']==0 for e in events if 'read_error' in e)
 assert [f['frame'] for f in frames]==[1,8,16,32] and any(f['nonblack_pixels'] for f in frames)
 results.append(dict(run=i,wall_seconds=time.monotonic()-start,header=fields,payload_sha256=sha(payload),frames=frames,events=events))
assert results[0]['payload_sha256']==results[1]['payload_sha256']
result=dict(identities=identities,runs=results)
(p/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
