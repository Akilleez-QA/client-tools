"""ONE separately parent-authorized runtime; never invoked during recipe preparation."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,signal,subprocess,sys,uuid
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
from cleanup import cleanup

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(x,message):
    if not x:raise RuntimeError(message)
def call(*args):return subprocess.check_output(args,text=True,timeout=15).strip()
def tree(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
def trace(text):
    require('FAIL' not in text and 'failure_cleanup' not in text,'probe recorded failure')
    pattern=r'^bind=(\S+) sample=(\S+) bytes=(\d+) return_s32=(-?\d+) return_bits=([0-9a-f]{8}) error_null=(\d+) error_terminated=(\d+) error_bytes=(\d+) error_hex=([0-9a-f]+|-)\s*$'
    binds=re.findall(pattern,text,re.M)
    require(len(binds)==5,'exact five binds')
    labels=['A1','B1','A2','F','B2-after-F'];sizes=[44144,88244,44144,44144,88244]
    identities=set()
    for i,b in enumerate(binds):
        label,pointer,size,value,bits,null,terminated,count,error=b
        require(label==labels[i] and int(size)==sizes[i],'bind label/extent')
        identities.add(pointer)
        require((int(value)&0xffffffff)==int(bits,16),'signed return bits')
        require((int(value)==0)==(label=='F'),'bind prerequisite, no retuning')
        require(terminated=='1' and null in ('0','1'),'owned error shape')
        raw=b'' if error=='-' else bytes.fromhex(error)
        require(len(raw)==int(count) and b'\0' not in raw and (null=='0' or not raw),'owned error content')
    require(len(identities)==1 and int(next(iter(identities)),16)!=0,'same nonnull sample identity')
    queries=re.findall(r'^query=(\S+) total_s32=(-?\d+) total_bits=([0-9a-f]{8}) current_s32=(-?\d+) current_bits=([0-9a-f]{8}) expected_total=(\d+) expected_current=0\s*$',text,re.M)
    require(len(queries)==4,'only four successful-bound queries')
    expected=[('A1',1000),('B1',2000),('A2',1000),('B2-after-F',2000)]
    for q,(name,msec) in zip(queries,expected):
        require(q[0]==name and int(q[1])==int(q[5])==msec and int(q[2],16)==msec and int(q[3])==int(q[4],16)==0,'PCM query expectation')
    events=[]
    for line in text.splitlines():
        if line.startswith(('bind=','query=','end=')):events.append(line.split()[0])
        elif line in ('release_returned','shutdown_returned'):events.append(line)
    wanted=[]
    for name in labels:
        wanted.append('bind='+name)
        if name!='F':wanted.extend(['query='+name,'end='+name])
    wanted.extend(['release_returned','shutdown_returned'])
    require(events==wanted,'exact operation observation order')
    require(text.count('PASS fixed same-sample PCM rebind characterization; all inputs alive through shutdown; no retirement proof')==1,'success marker')
    require('loaded_dll=c:\\binding30-private\\mss32.dll' in text.lower(),'loaded DLL path')
    startup=re.findall(r'^startup_s32=(-?\d+) startup_bits=([0-9a-f]{8})\s*$',text,re.M)
    require(len(startup)==1 and int(startup[0][0])!=0 and (int(startup[0][0])&0xffffffff)==int(startup[0][1],16),'startup prerequisite')
    return {'binds':binds,'queries':queries,'events':events}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--approved-runtime',action='store_true');ap.add_argument('--manifest-sha256',required=True)
    args=ap.parse_args();require(args.approved_runtime,'separate parent runtime approval required')
    require(sha(ROOT/'manifest.json')==args.manifest_sha256,'runtime manifest external pin')
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for p,h in manifest.items():require(sha(ROOT/p)==h,'runtime recipe identity: '+p)
    pins=json.loads((ROOT/'pins.json').read_text())
    receipt_path=BASE/'native-evidence-v1/receipt.json'
    require(sha(receipt_path)==pins['receipt_sha256'],'build receipt pin')
    receipt=json.loads(receipt_path.read_text());exe=BASE/'native-evidence-v1/probe.exe'
    require(receipt['cl_invocations']==1 and receipt['build_exit']==0 and receipt['stable_pinned_inputs'] and not receipt['executed'],'build prerequisites')
    require(sha(exe)==pins['exe_sha256']==receipt['output']['sha256'] and receipt['output']['machine']==332,'actual built PE pin')
    original=Path(pins['dll_path']);plugins=original.parent/'miles'
    require(sha(original)==pins['dll_sha256'] and tree(plugins)==pins['plugins'],'original DLL/plugin pins')
    with (ROOT/'attempt-v1.json').open('x') as f:json.dump({'pid':os.getpid(),'manifest':args.manifest_sha256},f)
    run=ROOT/('private-run-'+uuid.uuid4().hex[:8]);run.mkdir(mode=0o700)
    prefix=run/'prefix';name='swg_binding30_'+uuid.uuid4().hex[:10]
    result={'recipe_manifest':args.manifest_sha256,'receipt_sha256':pins['receipt_sha256'],'sink_name':name,'process_cleanup':[],'probe_invocations':0,'runtime_inputs':pins,'retirement_proof':False}
    env=os.environ.copy();env.update(WINEPREFIX=str(prefix),WINEDEBUG='-all',WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d')
    owned=[];wine_started=False;target=None
    def wine(args,log_name,timeout,cwd=None):
        nonlocal wine_started
        with (run/log_name).open('wb') as log:
            p=subprocess.Popen(args,env=env,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            owned.append((log_name,p));wine_started=True
            return p.wait(timeout=timeout)
    def terminate():
        errors=[]
        for tag,p in owned:
            record={'tag':tag,'pid':p.pid,'initial_exit':p.poll()}
            try:
                if p.poll() is None:
                    os.killpg(p.pid,signal.SIGTERM)
                    try:p.wait(timeout=3)
                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
                record['exit']=p.returncode
            except Exception as e:errors.append(str(e));record['error']=str(e)
            result['process_cleanup'].append(record)
        if wine_started:
            for option in ['-k','-w']:
                try:
                    with (run/('wineserver'+option+'.log')).open('wb') as log:subprocess.run(['wineserver',option],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=10,check=True)
                except Exception as e:errors.append(str(e))
        for tag,p in owned:
            try:p.wait(timeout=3)
            except Exception as e:errors.append(str(e))
        result['owned_children_reaped']=all(p.poll() is not None for _,p in owned)
        require(not errors,'; '.join(errors))
    def unload():
        modules=call('pactl','list','short','modules')
        for line in modules.splitlines():
            fields=line.split()
            if len(fields)>=2 and fields[1]=='module-null-sink' and 'sink_name='+name in fields:subprocess.run(['pactl','unload-module',fields[0]],timeout=15,check=True)
        result['owned_sink_absent']=all(len(l.split())<2 or l.split()[1]!=name for l in call('pactl','list','short','sinks').splitlines())
        require(result['owned_sink_absent'],'owned sink remains')
    def defaults():return {'sink':call('pactl','get-default-sink'),'source':call('pactl','get-default-source')}
    def write(value):
        (run/'results.json').write_text(json.dumps(value,indent=2)+'\n');print(run);print(json.dumps(value,indent=2))
    try:
        result['defaults_before']=defaults()
        seed=BASE.parent.parent/'miles-realtime/wine-prefix'
        require(seed.is_dir(),'existing owned seed prefix missing')
        subprocess.run(['cp','-a','--reflink=auto',str(seed),str(prefix)],timeout=30,check=True)
        result['owned_module']=call('pactl','load-module','module-null-sink','sink_name='+name,'rate=22050','channels=2','format=s16le')
        config=run/'alsa.conf';config.write_text('pcm.!default { type pulse server "unix:/run/user/'+str(os.getuid())+'/pulse/native" device "'+name+'" }\n')
        env.update(ALSA_CONFIG_PATH=str(config),PULSE_SINK=name,PULSE_SOURCE=name+'.monitor')
        require(wine(['wine','reg','add','HKCU\\Software\\Wine\\Drivers','/v','Audio','/d','alsa','/f'],'wine-config.log',15)==0,'private configuration failed')
        target=prefix/'drive_c/binding30-private';target.mkdir()
        shutil.copy2(original,target/'Mss32.dll');shutil.copytree(plugins,target/'miles');shutil.copy2(exe,target/'probe.exe')
        require(sha(target/'Mss32.dll')==pins['dll_sha256'] and sha(target/'probe.exe')==pins['exe_sha256'] and tree(target/'miles')==pins['plugins'],'staged input identity')
        for p,h in manifest.items():require(sha(ROOT/p)==h,'runtime recipe changed before launch')
        argv=['wine',str(target/'probe.exe'),'C:\\binding30-private\\Mss32.dll','C:\\binding30-private\\miles']
        result['command']=argv;result['probe_invocations']=1
        result['probe_exit']=wine(argv,'probe.log',15,target)
        require(result['probe_exit']==0,'probe nonzero exit: no retuning/retry')
        result['trace']=trace((run/'probe.log').read_text(errors='replace'))
        result['inputs_unchanged']=(sha(target/'Mss32.dll')==pins['dll_sha256'] and sha(target/'probe.exe')==pins['exe_sha256'] and tree(target/'miles')==pins['plugins'])
        require(result['inputs_unchanged'],'runtime input changed')
    except Exception as e:result['failure']={'type':type(e).__name__,'message':str(e)}
    finally:cleanup(terminate,unload,defaults,write,result)
    return 0 if not result.get('failure') and not result['cleanup_errors'] and result.get('defaults_unchanged') and result.get('owned_sink_absent') and result.get('owned_children_reaped') and result.get('inputs_unchanged') and result['probe_invocations']==1 and result.get('probe_exit')==0 else 1
if __name__=='__main__':raise SystemExit(main())
