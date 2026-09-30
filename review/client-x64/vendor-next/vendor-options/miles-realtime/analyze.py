from pathlib import Path
import json,re,hashlib
import numpy as np
base=Path(__file__).resolve().parent;rows=[];audio={}
for n in [2,3,4,5]:
 p=base/('run%d'%n);b=(p/'capture.s16').read_bytes();a=np.frombuffer(b,dtype='<i2').reshape(-1,2);nz=np.flatnonzero(np.any(a!=0,axis=1));audio[n]=a
 events=[dict(name=m[1],tick=int(m[2]),thread=int(m[3]),cw=m[4],mxcsr=m[5]) for m in re.finditer(r'event=(\S+) tick=(\d+) thread=(\d+) cw=(\w+) mxcsr=(\w+)',(p/'probe.log').read_text())];by={e['name']:e for e in events};r=json.load(open(p/'result.json'));r.update(run=n,bytes=len(b),pcm_seconds=len(a)/22050,sha256=hashlib.sha256(b).hexdigest(),nonzero_frames=len(nz),first_nonzero_frame=int(nz[0]) if len(nz) else None,last_nonzero_frame=int(nz[-1]) if len(nz) else None,events=events,sample_eos_ms=by['sample-eos']['tick']-by['sample-start']['tick'],stream_eos_ms=by['stream-eos']['tick']-by['stream-start']['tick']);rows.append(r)
ref=audio[2];first_ref=rows[0]['first_nonzero_frame'];pairs=[]
for row in rows[1:]:
 a=audio[row['run']];best=None
 # Compare 0.4 seconds beginning at reference's first signal, allowing a bounded residual shift around each measured first-signal alignment.
 for offset in range(-128,129):
  start=row['first_nonzero_frame']+offset
  if start<0:continue
  length=min(8820,len(a)-start,len(ref)-first_ref)
  diff=a[start:start+length].astype(np.int32)-ref[first_ref:first_ref+length].astype(np.int32);mse=float(np.mean(diff.astype(np.float64)**2))
  record=dict(run=row['run'],reference=2,lag_frames=int(start-first_ref),residual_offset=offset,compared_frames=length,differing_channel_samples=int(np.count_nonzero(diff)),max_abs=int(np.max(np.abs(diff))),rms=mse**.5)
  if best is None or mse<best[0]:best=(mse,record)
 pairs.append(best[1])
result=dict(runs=rows,comparisons=pairs,comparison_limit='Integer-frame alignment only, first0.4s signal window; timing gaps, resampling phase and truncated tails not normalized. No acceptance tolerance.')
(base/'repeat-analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(summary=[{k:r[k] for k in ['run','pcm_seconds','capture_wall_seconds','nonzero_frames','sample_eos_ms','stream_eos_ms']} for r in rows],comparisons=pairs),indent=2))
