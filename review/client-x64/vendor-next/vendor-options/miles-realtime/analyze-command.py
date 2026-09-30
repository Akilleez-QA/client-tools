from pathlib import Path
import numpy as np,json,re,wave,hashlib,struct
p=Path(__file__).resolve().parent
with wave.open(str(p.parent/'miles-probe/sample.wav'),'rb') as w: source=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)
rows=[];windows={}
for mode in ['sample','stream']:
 for route in ['direct','controller']:
  d=p/('command-'+route+'-'+mode);a=np.frombuffer((d/'capture.s16').read_bytes(),dtype='<i2').reshape(-1,2);n=1<<(len(a)+len(source)-2).bit_length();corr=np.fft.irfft(np.fft.rfft(a[:,0].astype(float),n)*np.fft.rfft(source[::-1],n),n)[len(source)-1:len(a)];offset=int(np.argmax(corr));seg=a[offset:offset+len(source)].astype(np.int32);windows[(mode,route)]=seg
  r=json.load(open(d/'result.json'));r.update(name=d.name,pcm_seconds=len(a)/22050,onset_aligned_frame=offset,asset_correlation=float(np.dot(seg[:,0],source)/np.sqrt(np.dot(seg[:,0].astype(float),seg[:,0])*np.dot(source,source))));r['events']=[dict(name=m[1],tick=int(m[2]),thread=int(m[3]),cw=m[4],mxcsr=m[5]) for m in re.finditer(r'event=(\S+) tick=(\d+) thread=(\d+) cw=(\w+) mxcsr=(\w+)',(d/'probe.log').read_text())];r['controller_events']=[l for l in (d/'probe.log').read_text().splitlines() if l.startswith('controller-')];rows.append(r)
comparisons=[]
for mode in ['sample','stream']:
 diff=windows[(mode,'controller')]-windows[(mode,'direct')];comparisons.append(dict(mode=mode,frames=len(source),differing_channel_samples=int(np.count_nonzero(diff)),max_abs=int(np.max(np.abs(diff))),rms=float(np.sqrt(np.mean(diff.astype(float)**2)))))
manifest={}
for name in ['miles-command-host.exe','miles-controller.exe','Mss32.dll','sample.wav','sample.mp3']:
 b=(p/'wine-prefix/drive_c/vendor-miles-probe'/name).read_bytes();rec=dict(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 if name.endswith(('.exe','.dll')):rec['machine']=hex(struct.unpack_from('<H',b,struct.unpack_from('<I',b,0x3c)[0]+4)[0])
 manifest[name]=rec
result=dict(runs=rows,comparisons=comparisons,manifest=manifest,limit='One command only; original x86 host unchanged between direct and x64-controlled route. Offset/4488-frame trim only. No tolerance, no callback RPC or game integration.')
(p/'command-analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(summary=[{k:r[k] for k in ['name','returncode','pcm_seconds','capture_wall_seconds','asset_correlation','controller_events']} for r in rows],comparisons=comparisons,manifest=manifest),indent=2))
