import os, subprocess, time, json, uuid, hashlib, shutil
from pathlib import Path
base=Path(__file__).resolve().parent
prefix=base/'private-prefix-engine-v2'
old=base.parent/'miles-realtime/wine-prefix'
out=base/'run-v2';out.mkdir()
commands=[]
def call(*args,env=None):
 commands.append(list(args));return subprocess.check_output(args,env=env,text=True,timeout=15).strip()
def save():
 (out/'commands.json').write_text(json.dumps(commands,indent=2))
 (out/'results.json').write_text(json.dumps(result,indent=2))
result={};module=None;player=None
name='swg_engine_'+uuid.uuid4().hex[:12]
env=os.environ.copy();env.update(WINEPREFIX=str(prefix),WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d',WINEDEBUG='-all')
try:
 result['defaults_before']={k:call('pactl','get-default-'+k) for k in ['sink','source']}
 assert not prefix.exists()
 call('cp','-a','--reflink=auto',str(old),str(prefix))
 target=prefix/'drive_c/engine-private';target.mkdir(exist_ok=True)
 shutil.copy2(base/'probe.exe',target/'probe.exe')
 original=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll')
 assert hashlib.sha256(original.read_bytes()).hexdigest()=='0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
 shutil.copy2(original,target/'Mss32.dll');shutil.copy2(base.parent/'miles-probe/sample.wav',target/'sample.wav');shutil.copy2(base.parent/'miles-probe/sample.wav',target/'second.wav')
 shutil.copytree(original.parent/'miles',target/'miles',dirs_exist_ok=True)
 manifest=Path('/home/akilleez/Work/swg-source/clientdata_OLD/datatables/manifest/skufree.iff')
 (target/'datatables/manifest').mkdir(parents=True,exist_ok=True)
 shutil.copy2(manifest,target/'datatables/manifest/skufree.iff')
 shutil.copytree(base/'private-support/data_other_00/datatables/music',target/'datatables/music',dirs_exist_ok=True)
 result['manifest_asset']={'source':str(manifest),'sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}
 (target/'probe.cfg').write_text('[ClientAudio]\nenabled=true\n[SharedFile]\nsearchPath0=.\n')
 assert hashlib.sha256((target/'sample.wav').read_bytes()).hexdigest()=='ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9'
 result['hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [base/'probe.cpp',base/'probe.exe',base/'build.py',base/'run.py',original,target/'Mss32.dll',target/'sample.wav']}
 result['wine']=call('wine','--version')
 module=call('pactl','load-module','module-null-sink','sink_name='+name,'rate=22050','channels=2','format=s16le');result['module']=module;result['sink_name']=name
 sink=next(x for x in json.loads(call('pactl','-f','json','list','sinks')) if x['name']==name)
 result['sink']=sink
 assert str(sink['owner_module'])==module
 assert sink['properties'].get('factory.name')=='support.null-audio-sink',sink
 conf=out/'alsa-private.conf';conf.write_text('pcm.!default {\n type pulse\n server "unix:/run/user/'+str(os.getuid())+'/pulse/native"\n device "'+name+'"\n}\n')
 env.update(ALSA_CONFIG_PATH=str(conf),PULSE_SINK=name,PULSE_SOURCE=name+'.monitor')
 cmd=['wine','reg','add','HKCU\\Software\\Wine\\Drivers','/v','Audio','/d','alsa','/f'];commands.append(cmd)
 with (out/'wine-config.log').open('wb') as log:subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=30,check=True)
 result['runs']=[]
 for label in ['engine-baseline-1']:
  rec={'label':label,'routing':[]};result['runs'].append(rec)
  cmd=['wine',str(target/'probe.exe')];commands.append(cmd)
  with (out/(label+'.log')).open('wb') as log:
   start=time.monotonic();player=subprocess.Popen(cmd,env=env,cwd=target,stdout=log,stderr=subprocess.STDOUT)
   while player.poll() is None and time.monotonic()-start<15:
    inputs=json.loads(call('pactl','-f','json','list','sink-inputs'))
    rec['routing'].append({'seconds':time.monotonic()-start,'inputs':[x for x in inputs if x['sink']==sink['index']], 'all_inputs':inputs})
    time.sleep(.025)
   if player.poll() is None:rec['timed_out']=True;player.kill()
   rec['returncode']=player.wait(timeout=5);rec['wall_seconds']=time.monotonic()-start
  save()
  rec['producer_observed']=any(x['inputs'] for x in rec['routing'])
  save()
except Exception as e:
 result['failure']=repr(e)
 raise
finally:
 if player and player.poll() is None:player.kill();player.wait(timeout=5)
 if prefix.exists():
  commands.append(['wineserver','-k']); result['private_wineserver_stop']=subprocess.run(['wineserver','-k'],env=env,timeout=10).returncode
 if module:result['unload']=call('pactl','unload-module',module)
 result['defaults_after']={k:call('pactl','get-default-'+k) for k in ['sink','source']}
 result['defaults_unchanged']=result.get('defaults_before')==result['defaults_after']
 result['sink_removed']=name not in [x['name'] for x in json.loads(call('pactl','-f','json','list','sinks'))]
 save()
print(json.dumps({k:v for k,v in result.items() if k not in ['runs','sink','hashes']},indent=2))
