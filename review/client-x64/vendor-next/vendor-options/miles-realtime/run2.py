import os,subprocess,time,json,uuid,hashlib,shutil,signal
from pathlib import Path
base=Path(__file__).resolve().parent;old=base.parent/'miles-probe';out=base/'run2';out.mkdir(exist_ok=False);prefix=base/'wine-prefix'
if not prefix.exists(): subprocess.run(['cp','-a','--reflink=auto',str(old/'wine-prefix'),str(prefix)],check=True)
def call(*a):return subprocess.check_output(a,text=True).strip()
before=dict(sink=call('pactl','get-default-sink'),source=call('pactl','get-default-source'))
name='swg_miles_'+uuid.uuid4().hex[:12];module=None;capture=None;player=None;records=[];env=os.environ.copy();env.update(WINEPREFIX=str(prefix),WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d',WINEDEBUG='-all');result=dict(defaults_before=before,sink=name,format='s16le',rate=22050,channels=2)
try:
 module=call('pactl','load-module','module-null-sink','sink_name='+name,'rate=22050','channels=2','format=s16le');result['module']=module
 sink=next(x for x in json.loads(call('pactl','-f','json','list','sinks')) if x['name']==name);result['sink_index']=sink['index']
 conf=out/'alsa-pulse.conf';conf.write_text('pcm.!default {\n type pulse\n server "unix:/run/user/1000/pulse/native"\n device "'+name+'"\n}\n');env['ALSA_CONFIG_PATH']=str(conf);env['PULSE_SINK']=name;env['PULSE_SOURCE']=name+'.monitor'
 # ALSA driver is already selected in copied disposable prefix; no host registry or defaults change.
 subprocess.run(['wine','reg','add','HKCU\\Software\\Wine\\Drivers','/v','Audio','/d','alsa','/f'],env=env,stdout=(out/'wine-config.log').open('wb'),stderr=subprocess.STDOUT,timeout=30,check=True)
 raw=(out/'capture.s16').open('wb');caplog=(out/'capture.log').open('wb');start=time.monotonic();capture=subprocess.Popen(['parec','--device='+name+'.monitor','--format=s16le','--rate=22050','--channels=2','--raw','--latency-msec=20','--process-time-msec=10'],stdout=raw,stderr=caplog)
 log=(out/'probe.log').open('wb');player=subprocess.Popen(['wine',str(prefix/'drive_c/vendor-miles-probe/probe.exe'),'C:\\vendor-miles-probe\\Mss32.dll','C:\\vendor-miles-probe\\sample.wav','C:\\vendor-miles-probe\\sample.mp3'],env=env,cwd=out,stdout=log,stderr=subprocess.STDOUT)
 deadline=start+20
 while player.poll() is None and time.monotonic()<deadline:
  own=[x for x in json.loads(call('pactl','-f','json','list','sink-inputs')) if x.get('sink')==sink['index']]
  records.append(dict(seconds=time.monotonic()-start,bytes=(out/'capture.s16').stat().st_size,inputs=[dict(index=x['index'],sink=x['sink'],sample_specification=x.get('sample_specification'),name=x.get('properties',{}).get('application.name'),mute=x.get('mute'),volume=x.get('volume')) for x in own]));time.sleep(.05)
 if player.poll() is None:player.kill();result['timed_out']=True
 result['returncode']=player.wait(timeout=5);result['probe_wall_seconds']=time.monotonic()-start
 # Explicit bounded drain/capture clock observation; no audio physical route.
 end=time.monotonic()+3
 while time.monotonic()<end:records.append(dict(seconds=time.monotonic()-start,bytes=(out/'capture.s16').stat().st_size));time.sleep(.05)
 result['capture_wall_seconds']=time.monotonic()-start
finally:
 if player and player.poll() is None:player.kill();player.wait()
 if capture and capture.poll() is None:capture.terminate();capture.wait(timeout=5)
 if module:subprocess.run(['pactl','unload-module',module],check=True)
 result['defaults_after']=dict(sink=call('pactl','get-default-sink'),source=call('pactl','get-default-source'));result['defaults_unchanged']=result['defaults_after']==before
 (out/'clock.json').write_text(json.dumps(records,indent=2));(out/'result.json').write_text(json.dumps(result,indent=2));print(result)
