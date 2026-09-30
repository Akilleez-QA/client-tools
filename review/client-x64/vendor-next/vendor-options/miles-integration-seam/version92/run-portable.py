from pathlib import Path
import hashlib,json,os,subprocess,sys
if sys.argv[1:]!=['--approved-portable']:raise SystemExit('Separate parent approval required')
b=Path(__file__).resolve().parent;m=json.loads((b/'manifest.json').read_text())['sha256']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def changed():return [n for n,h in m.items() if sha(b/n)!=h]
if changed():raise RuntimeError('Frozen inputs changed')
o=b/'evidence-v1';o.mkdir(exist_ok=False)
r={'passed':False,'scope':'actual version90 Core/Session/codec; explicit Channel/Runtime substitutes; no native API or real return join','runs':[]}
env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1:abort_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1:print_stacktrace=1'
def run(cmd,name,limit):
 (o/(name+'-command.json')).write_text(json.dumps(cmd,indent=2)+'\n')
 with (o/(name+'.log')).open('wb') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=limit)
 if p.returncode:raise RuntimeError(name+' failed exit'+str(p.returncode))
try:
 sources=['tests.cpp','tree/transport-candidate/codec.cpp','tree/session-version22/session_version.cpp','tree/startup-metadata-v4/metadata_wire.cpp','tree/callback-reentry47/invocation_guard.cpp']
 run(['/usr/bin/clang++','-std=c++11','-Wall','-Wextra','-Wpedantic','-Werror','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer','-include',str(b/'compat.h')]+[str(b/n) for n in sources]+['-o',str(o/'tests')],'build',120)
 for mode in ['normal','oversize','nonterminated','missing','legacy_text','callback','context']:
  run([str(o/'tests'),mode],mode,30)
  lines=(o/(mode+'.log')).read_text().splitlines()
  if len(lines)!=1 or not lines[0].startswith('PASS '+mode+' checks='):raise RuntimeError('Unexpected output '+mode)
  r['runs'].append(mode)
 r['passed']=True
except Exception as e:r['failure']=repr(e)
finally:
 r['changed']=changed();r['passed']=r['passed'] and not r['changed'];(o/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
sys.exit(0 if r['passed'] else 1)
