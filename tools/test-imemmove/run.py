#!/usr/bin/env python3
"""Native v120 real-header overlap probe; Debug is deliberately compile-only."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--bits',type=int,choices=[32,64],required=True)
    p.add_argument('--configuration',choices=['Debug','Release'],required=True)
    p.add_argument('--baseline',action='store_true')
    p.add_argument('--expect-ambiguity',action='store_true')
    a=p.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    r={'passed':False,'runtime_executed':False,'bits':a.bits,'configuration':a.configuration,'baseline':a.baseline}
    try:
        if a.expect_ambiguity and not (a.baseline and a.bits==64): raise ValueError('ambiguity control requires baseline x64')
        checkout=a.checkout.resolve(); header=checkout/'src/engine/shared/library/sharedFoundation/src/shared/Misc.h'
        probe=Path(__file__).with_name('probe.cpp').resolve();compiler=shutil.which('cl')
        if not compiler: raise ValueError('use the matching VS2013 developer prompt')
        r['inputs']={str(x):sha(x) for x in [header,probe,Path(__file__).resolve(),Path(compiler)]}
        command=[compiler,'/nologo','/EHsc','/W3','/showIncludes','/DWIN32','/DPLATFORM_WIN32','/DCOMPILE_DLL=1','/DEXPECT_BITS='+str(a.bits),'/I'+str(checkout/'src/engine/shared/library/sharedFoundation/include/public'),'/Fo'+str(out/'probe.obj'),str(probe)]
        if a.baseline: command.append('/DTEST_BASELINE')
        if a.configuration=='Debug': command+=['/D_DEBUG','/MTd','/c']
        else: command+=['/MT','/Fe'+str(out/'probe.exe')]
        r['command']=command
        x=subprocess.run(command,cwd=out,env=dict(os.environ,VSLANG='1033'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (out/'build.log').write_bytes(x.stdout);r['build_exit']=x.returncode
        text=x.stdout.decode('utf-8','replace')
        r['included_headers']={s.strip():sha(s.strip()) for s in re.findall(r'Note: including file:\s*(.+)',text)}
        if a.expect_ambiguity:
            if x.returncode==0 or 'C2668' not in text or 'memmove' not in text: raise ValueError('expected native memmove ambiguity was not observed')
            r['observed_expected_ambiguity']=True
        else:
            if x.returncode: raise ValueError('build failed; see build.log')
            if a.configuration=='Release':
                r['runtime_executed']=True
                x=subprocess.run([str(out/'probe.exe')],cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
                (out/'run.log').write_bytes(x.stdout);r['run_exit']=x.returncode
                if x.returncode or x.stdout.decode('ascii','replace').splitlines().count('PASS 30 valid overlap and overload checks')!=1: raise ValueError('unexpected runtime result/count')
                r['checks']=30
            else:r['scope']='real Debug header object compile only; engine DebugFatal runtime not linked'
        r['passed']=True
    except Exception as e:r['error']=str(e)
    (out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    return 0 if r['passed'] else 1
if __name__=='__main__':sys.exit(main())
