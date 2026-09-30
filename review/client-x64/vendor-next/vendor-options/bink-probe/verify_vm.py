import subprocess,pathlib,hashlib,json,struct
p=pathlib.Path('C:/vendor-bink-probe'); results=[]
for i in range(2):
 r=subprocess.run([str(p/'driver64.exe')],capture_output=True,timeout=60,cwd=p)
 (p/('seam-%d.raw'%i)).write_bytes(r.stdout)
 header,payload=r.stdout.split(b'\n',1); fields=dict(x.split('=',1) for x in header.decode().split()[1:])
 h=14695981039346656037
 for v in payload:h=((h^v)*1099511628211)&((1<<64)-1)
 assert len(payload)==int(fields['length']) and '%016x'%h==fields['fnv1a64'] and fields['pointer_bytes']=='8' and fields['child_exit']=='0' and r.returncode==0
 events=[json.loads(line) for line in payload.splitlines()]
 assert events[0]['pointer_bytes']==4 and events[1]['event']=='no_asset_decode_not_run'
 results.append(dict(run=i,header=fields,payload_sha256=hashlib.sha256(payload).hexdigest(),events=events))
assert results[0]['payload_sha256']==results[1]['payload_sha256']
for name in ['probe32.exe','driver64.exe','binkw32.dll']:
 b=(p/name).read_bytes(); pe=struct.unpack_from('<I',b,60)[0]; print(json.dumps(dict(file=name,sha256=hashlib.sha256(b).hexdigest(),machine=hex(struct.unpack_from('<H',b,pe+4)[0]))))
(p/'seam-verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
