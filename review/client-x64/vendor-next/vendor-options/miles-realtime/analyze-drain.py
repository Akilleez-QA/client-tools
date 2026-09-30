from pathlib import Path
import numpy as np
def correlate(a,b,mode=None,method=None):
 n=1 << (len(a)+len(b)-2).bit_length()
 return np.fft.irfft(np.fft.rfft(a,n)*np.fft.rfft(b[::-1],n),n)[len(b)-1:len(a)]
import wave,json,re,hashlib
p=Path(__file__).resolve().parent
with wave.open(str(p.parent/'miles-probe/sample.wav'),'rb') as w: source=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)
rows=[];windows={}
for mode in ['sample','stream']:
 for n in range(1,4):
  d=p/('drain-'+mode+'-'+str(n))
  if not (d/'result.json').exists():continue
  raw=(d/'capture.s16').read_bytes();audio=np.frombuffer(raw,dtype='<i2').reshape(-1,2);c=correlate(audio[:,0].astype(float),source,mode='valid',method='fft');start=int(np.argmax(c));seg=audio[start:start+len(source)].astype(np.int32);windows[(mode,n)]=seg
  nz=np.flatnonzero(np.any(audio!=0,axis=1));r=json.load(open(d/'result.json'));r.update(name=d.name,frames=len(audio),pcm_seconds=len(audio)/22050,signal_first=int(nz[0]),signal_last=int(nz[-1]),nonzero_frames=len(nz),asset_frames=len(source),asset_alignment_start=start,asset_correlation=float(np.dot(seg[:,0],source)/np.sqrt(np.dot(seg[:,0].astype(float),seg[:,0])*np.dot(source,source))),asset_window_nonzero=int(np.count_nonzero(np.any(seg!=0,axis=1))),sha256=hashlib.sha256(raw).hexdigest())
  events=[dict(name=m[1],tick=int(m[2]),thread=int(m[3]),cw=m[4],mxcsr=m[5]) for m in re.finditer(r'event=(\S+) tick=(\d+) thread=(\d+) cw=(\w+) mxcsr=(\w+)',(d/'probe.log').read_text())];r['events']=events;rows.append(r)
comparisons=[]
for mode in ['sample','stream']:
 for n in [2,3]:
  if (mode,n) not in windows:continue
  diff=windows[(mode,n)]-windows[(mode,1)];comparisons.append(dict(mode=mode,run=n,reference=1,differing_channel_samples=int(np.count_nonzero(diff)),max_abs=int(np.max(np.abs(diff))),rms=float(np.sqrt(np.mean(diff.astype(float)**2)))))
result=dict(runs=rows,comparisons=comparisons,limits='Only integer-frame offset and exact4488-frame asset window; raw bytes retained. No amplitude normalization, resampling, noise filtering or tolerance. Correlation identifies clip; not equality proof.')
(p/'drain-analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(summary=[{k:r[k] for k in ['name','asset_correlation','nonzero_frames','asset_window_nonzero','pcm_seconds','capture_wall_seconds']} for r in rows],comparisons=comparisons),indent=2))
