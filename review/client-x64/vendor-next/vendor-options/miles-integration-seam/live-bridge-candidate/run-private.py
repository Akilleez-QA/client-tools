from pathlib import Path
import os,subprocess,json,hashlib,uuid,shutil
base=Path(__file__).resolve().parent;run=base/('private-run-'+uuid.uuid4().hex[:8]);run.mkdir();prefix=run/'prefix'
old=base.parent.parent/'miles-realtime/wine-prefix'
subprocess.run(['cp','-a','--reflink=auto',str(old),str(prefix)],check=True)
def call(*args):return subprocess.check_output(args,text=True,timeout=15).strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll');wav=base.parent.parent/'miles-probe/sample.wav'
assert digest(original)=='0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
assert digest(wav)=='ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9'
before={'sink':call('pactl','get-default-sink'),'source':call('pactl','get-default-source')};name='swg_bridge_live_'+uuid.uuid4().hex[:10];module=None
result={'defaults_before':before,'sink_name':name,'runs':[],'private_inputs':{'dll':digest(original),'wav':digest(wav)}}
env=os.environ.copy();env.update(WINEPREFIX=str(prefix),WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d',WINEDEBUG='-all')
try:
 module=call('pactl','load-module','module-null-sink','sink_name='+name,'rate=22050','channels=2','format=s16le');result['owned_module']=module
 config=run/'alsa.conf';config.write_text('pcm.!default { type pulse server "unix:/run/user/'+str(os.getuid())+'/pulse/native" device "'+name+'" }\n');env.update(ALSA_CONFIG_PATH=str(config),PULSE_SINK=name,PULSE_SOURCE=name+'.monitor')
 with (run/'wine-config.log').open('wb') as log:subprocess.run(['wine','reg','add','HKCU\\Software\\Wine\\Drivers','/v','Audio','/d','alsa','/f'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=30,check=True)
 target=prefix/'drive_c/bridge-live-private';target.mkdir(exist_ok=True)
 shutil.copy2(original,target/'Mss32.dll');shutil.copy2(wav,target/'sample.wav')
 for cfg in ['Debug','Release']:
  host=base/'native-v2'/('x86-'+cfg)/'host.exe';controller=base/'native-v2'/('amd64-'+cfg)/'controller.exe'
  shutil.copy2(host,target/'host.exe');shutil.copy2(controller,target/'controller.exe')
  with (run/(cfg+'.log')).open('wb') as log:
   try:p=subprocess.run(['wine',str(target/'controller.exe'),'C:\\bridge-live-private\\host.exe','C:\\bridge-live-private\\sample.wav'],env=env,cwd=target,stdout=log,stderr=subprocess.STDOUT,timeout=30);code=p.returncode
   except subprocess.TimeoutExpired:code='timeout';subprocess.run(['wineserver','-k'],env=env,timeout=10)
  if (target/'host.log').exists():shutil.copy2(target/'host.log',run/(cfg+'-host.log'))
  text=(run/(cfg+'.log')).read_text(errors='replace');hosttext=(run/(cfg+'-host.log')).read_text(errors='replace') if (run/(cfg+'-host.log')).exists() else ''
  rec={'config':cfg,'returncode':code,'host_sha256':digest(host),'controller_sha256':digest(controller),'exact_count':'PASS 21 framed requests' in text,'cleanup':'PASS host ordered shutdown' in hosttext,'loaded_exact':'loaded_dll=C:\\bridge-live-private\\Mss32.dll'.lower() in hosttext.lower()};result['runs'].append(rec)
  if code!=0:break

finally:
 subprocess.run(['wineserver','-k'],env=env,timeout=10)
 if module:subprocess.run(['pactl','unload-module',module],check=True,timeout=15)
 result['defaults_after']={'sink':call('pactl','get-default-sink'),'source':call('pactl','get-default-source')};result['defaults_unchanged']=before==result['defaults_after'];result['source_sha256']={p.name:digest(p) for p in base.glob('*.cpp')};(run/'results.json').write_text(json.dumps(result,indent=2));print(run);print(json.dumps(result))
raise SystemExit(not result['defaults_unchanged'] or len(result['runs'])!=2 or any(x['returncode']!=0 or not x['exact_count'] or not x['cleanup'] or not x['loaded_exact'] for x in result['runs']))
