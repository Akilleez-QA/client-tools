"""Private real-asset decoder comparison. No tolerance pass is assigned."""
from pathlib import Path
import hashlib,json,wave,numpy as np
p=Path(__file__).resolve().parent
def load(name):
 with wave.open(str(p/name),'rb') as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,w.getnchannels()),dict(channels=w.getnchannels(),rate=w.getframerate(),width=w.getsampwidth(),frames=w.getnframes())
a,meta=load('decoded-original.wav');b,bmeta=load('decoded-ffmpeg.wav');c=np.fromfile(p/'decoded-miniaudio.s16',dtype='<i2').reshape(-1,2)
assert meta['channels']==bmeta['channels']==2 and meta['rate']==bmeta['rate']==44100 and meta['width']==bmeta['width']==2
results={}
for name,x in [('ffmpeg',b),('miniaudio',c)]:
 best=None
 for off in range(-4096,4097):
  start=max(0,-off)+4096;end=min(len(a),len(x)-off,start+44100)
  delta=a[start:end].astype(np.int32)-x[start+off:end+off].astype(np.int32);mse=float(np.mean(delta.astype(float)**2))
  if best is None or mse<best[0]:best=(mse,off)
 off=best[1];start=max(0,-off);end=min(len(a),len(x)-off);delta=a[start:end].astype(np.int32)-x[start+off:end+off].astype(np.int32)
 results[name]=dict(frames=len(x),best_offset_candidate_minus_original=off,overlap_frames=end-start,unequal_samples=int(np.count_nonzero(delta)),total_samples=delta.size,max_abs_error=int(np.abs(delta).max()),rms_error=float(np.sqrt(np.mean(delta.astype(float)**2))),trim_original_front=start,trim_candidate_front=start+off,original_tail=len(a)-end,candidate_tail=len(x)-(end+off))
result=dict(original=meta,ffmpeg=bmeta,miniaudio_log=(p/'miniaudio-decode.log').read_text(),comparison=results,files={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['sample.mp3','decoded-original.wav','decoded-ffmpeg.wav','decoded-miniaudio.s16','miniaudio-decode.c']})
(p/'decoder-comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
