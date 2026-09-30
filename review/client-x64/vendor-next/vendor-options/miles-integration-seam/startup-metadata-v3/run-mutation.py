if not __debug__:
 raise SystemExit("Optimized Python is prohibited before any runtime activity")
from pathlib import Path
import os,subprocess,json,hashlib,uuid,shutil
from cleanup import cleanup
base=Path(__file__).resolve().parent;run=base/('private-wrongpath-'+uuid.uuid4().hex[:8]);run.mkdir();prefix=run/'prefix'
old=base.parent.parent/'miles-realtime/wine-prefix'
subprocess.run(['cp','-a','--reflink=auto',str(old),str(prefix)],check=True)
def call(*args):return subprocess.check_output(args,text=True,timeout=15).strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll');wav=base.parent.parent/'miles-probe/sample.wav'
assert digest(original)=='0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
assert digest(wav)=='ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9'
before={'sink':call('pactl','get-default-sink'),'source':call('pactl','get-default-source')};name='swg_startup_'+uuid.uuid4().hex[:10];module=None
receipt_path=base/'native-wrongpath/receipt.json';receipt_pin='90801dc2e5c09723119953f3b024309df258590c278685734a1d5b8befeee768';assert digest(receipt_path)==receipt_pin;receipt=json.loads(receipt_path.read_text());assert receipt['builder_before']==receipt['builder_after']
result={'receipt_sha256':receipt_pin,'defaults_before':before,'sink_name':name,'runs':[],'private_inputs':{'dll':digest(original),'wav':digest(wav)}}
env=os.environ.copy();env.update(WINEPREFIX=str(prefix),WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d',WINEDEBUG='-all')
try:
 module=call('pactl','load-module','module-null-sink','sink_name='+name,'rate=22050','channels=2','format=s16le');result['owned_module']=module
 config=run/'alsa.conf';config.write_text('pcm.!default { type pulse server "unix:/run/user/'+str(os.getuid())+'/pulse/native" device "'+name+'" }\n');env.update(ALSA_CONFIG_PATH=str(config),PULSE_SINK=name,PULSE_SOURCE=name+'.monitor')
 with (run/'wine-config.log').open('wb') as log:subprocess.run(['wine','reg','add','HKCU\\Software\\Wine\\Drivers','/v','Audio','/d','alsa','/f'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=30,check=True)
 target=prefix/'drive_c/startup-private';target.mkdir(exist_ok=True)
 shutil.copy2(original,target/'Mss32.dll');shutil.copytree(original.parent/'miles',target/'miles')
 for cfg in ['Debug','Release']:
  exe=base/'native-wrongpath'/('x86-'+cfg+'-host')/'test.exe';build=[x for x in receipt['builds'] if x['arch']=='x86' and x['kind']=='host' and x['config']==cfg][0];assert build['exit_code']==0 and build['inputs_unchanged'] and build['before']==build['after'];assert digest(exe)==build['output']['sha256'];shutil.copy2(exe,target/'probe.exe');assert digest(target/'probe.exe')==build['output']['sha256']
  with (run/(cfg+'.log')).open('wb') as log:
   try:p=subprocess.run(['wine',str(target/'probe.exe')],env=env,cwd=target,stdout=log,stderr=subprocess.STDOUT,timeout=20);code=p.returncode
   except subprocess.TimeoutExpired:code='timeout';subprocess.run(['wineserver','-k'],env=env,timeout=10)
  text=(run/(cfg+'.log')).read_text(errors='replace');rec={'config':cfg,'returncode':code,'exe_sha256':digest(exe),'exact_count':'32/33 genuine metadata checks; same-vendor oracle, no playback' in text,'cleanup':'CLEANUP preference_restore_called=1 shutdown_called=1' in text,'loaded_exact':'loaded_dll=C:\\startup-private\\Mss32.dll'.lower() in text.lower()};result['runs'].append(rec)
  if code!=1:break
finally:
 def write_result(value):
  value['source_provenance']='pinned build receipt before/after inputs; no mutable post-run source hashing'
  (run/'results.json').write_text(json.dumps(value,indent=2));print(run);print(json.dumps(value))
 cleanup(lambda:subprocess.run(['wineserver','-k'],env=env,timeout=10,check=True),
         lambda:subprocess.run(['pactl','unload-module',module],check=True,timeout=15) if module else None,
         lambda:{'sink':call('pactl','get-default-sink'),'source':call('pactl','get-default-source')},
         write_result,result)

raise SystemExit(result['cleanup_errors'] or not result.get('defaults_unchanged',False) or len(result['runs'])!=2 or any(x['returncode']!=1 or not x['exact_count'] or not x['cleanup'] or not x['loaded_exact'] for x in result['runs']))
