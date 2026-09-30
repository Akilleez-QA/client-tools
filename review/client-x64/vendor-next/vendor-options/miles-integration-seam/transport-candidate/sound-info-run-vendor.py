from pathlib import Path
import subprocess,json,hashlib
r=Path('C:/miles-sound-info-valid-v2');src=r/'transport-candidate';results=[]
expected={'Mss32.dll':'0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe','sample.wav':'ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9'}
for n,h in expected.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
for cfg in ['Debug','Release']:
 for arch in ['x86','amd64']:
  out=r/(arch+'-'+cfg);out.mkdir(exist_ok=True);cmd=out/'build.cmd';exe=out/'test.exe'
  cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncd /d "'+str(out)+'"\ncl /nologo /EHsc /W4 /WX /DWIN32 /IC:/client-next-build/src/external/3rd/library/miles/include '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' "'+str(src/'sound-info-codec.cpp')+'" "'+str(src/'sound-info-vendor-test.cpp')+'" /Fe"'+str(exe)+'"\n')
  p=subprocess.run(['cmd','/d','/c',str(cmd)],capture_output=True,timeout=60);(out/'compile.log').write_bytes(p.stdout+p.stderr)
  rec=dict(config=cfg,arch=arch,compile_exit=p.returncode);results.append(rec)
  if p.returncode:continue
  peer=r/('x86-'+cfg);args=[str(exe),str(r/'sample.wav'),str(peer/'metadata.bin'),str(peer/'expected.txt'),str(r/'Mss32.dll')]
  p=subprocess.run(args,capture_output=True,timeout=15,cwd=out);log=p.stdout+p.stderr;(out/'run.log').write_bytes(log);rec.update(run_exit=p.returncode,command=args,success=b'PASS 11 scalar/offset fields' in log)
  if arch=='x86':rec['loaded_exact']=('loaded_dll='+str(r/'Mss32.dll')).replace('/','\\').encode().lower() in log.lower()
for n,h in expected.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
(r/'results.json').write_text(json.dumps({'results':results,'private_inputs_sha256':expected,'source_sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['transport-candidate','protocol-candidate'] for p in (r/d).glob('*') if p.is_file()}},indent=2));print(results)
raise SystemExit(any(x.get('compile_exit') or x.get('run_exit',1) or not x.get('success') or x.get('loaded_exact',True)==False for x in results))
