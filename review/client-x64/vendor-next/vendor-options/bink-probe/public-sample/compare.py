from pathlib import Path
import hashlib,json,collections,array,zlib
p=Path(__file__).resolve().parent; private=p.parent/'private/public-sample'
sha=lambda b:hashlib.sha256(b).hexdigest()
v=json.loads((p/'verification.json').read_text())
for run in range(2):
 raw=(private/('decode-%d.raw'%run)).read_bytes();header,payload=raw.split(b'\n',1)
 fields=dict(x.split('=',1) for x in header.decode().split()[1:]);h=14695981039346656037
 for c in payload:h=((h^c)*1099511628211)&((1<<64)-1)
 assert int(fields['length'])==len(payload) and fields['fnv1a64']=='%016x'%h
 assert sha(payload)==v['runs'][run]['payload_sha256']
 off=0;frames=[]
 while off<len(payload):
  end=payload.index(b'\n',off);event=json.loads(payload[off:end]);off=end+1
  if event.get('kind')=='pixels':
   n=event['length'];data=payload[off:off+n];off+=n;assert payload[off:off+1]==b'\n';off+=1
   assert data==(private/('frame-%02d.bgra'%event['frame'])).read_bytes();frames.append(event['frame'])
 assert frames==[1,8,16,32]
reference=(private/'ffmpeg.bgra').read_bytes();size=640*480*4;assert len(reference)==4*size
assert reference==(private/'ffmpeg-bounded.bgra').read_bytes()
out=[]
for i,f in enumerate([1,8,16,32]):
 a=(private/('frame-%02d.bgra'%f)).read_bytes();b=reference[i*size:(i+1)*size];assert len(a)==len(b)==size
 assert sha(a)==v['runs'][0]['frames'][i]['sha256']
 delta=array.array('h',(x-y for x,y in zip(a,b)))
 import sys
 if sys.byteorder!='little':delta.byteswap()
 diffpath=private/('delta-old-minus-ffmpeg-%02d.s16le.zlib'%f);diffpath.write_bytes(zlib.compress(delta.tobytes()));assert zlib.decompress(diffpath.read_bytes())==delta.tobytes()
 channels={}
 for c,name in enumerate('BGRA'):
  aa=a[c::4];bb=b[c::4];hist=collections.Counter(x-y for x,y in zip(aa,bb))
  channels[name]=dict(old_min=min(aa),old_max=max(aa),ffmpeg_min=min(bb),ffmpeg_max=max(bb),differing_bytes=sum(n for d,n in hist.items() if d),max_abs_error=max(map(abs,hist)),mean_abs_error=sum(abs(d)*n for d,n in hist.items())/len(aa),signed_difference_histogram=dict(sorted(hist.items())))
 def nonblack(buf,threshold):return sum(max(buf[j:j+3])>threshold for j in range(0,len(buf),4))
 out.append(dict(frame=f,old_sha256=sha(a),ffmpeg_sha256=sha(b),exact_equal=a==b,rgb_differing_pixels=sum(a[j:j+3]!=b[j:j+3] for j in range(0,size,4)),alpha_differing_pixels=channels['A']['differing_bytes'],old_nonblack_pixels=nonblack(a,0),old_pixels_above_16=nonblack(a,16),ffmpeg_nonblack_pixels=nonblack(b,0),ffmpeg_pixels_above_16=nonblack(b,16),channels=channels,complete_difference_file=str(diffpath.relative_to(p.parent)),difference_sha256=sha(diffpath.read_bytes())))
(p/'comparison.json').write_text(json.dumps(dict(oracle_sha256=sha((p.parent/'oracle.md').read_bytes()),transport_revalidated_on_linux=True,frames=out),indent=2))
for r in out:print(json.dumps({k:v for k,v in r.items() if k not in ('channels','complete_difference_file','difference_sha256')}))
