#!/usr/bin/env python3
"""Prospective host-only symbol resolution. Never executes the output."""
from pathlib import Path
import hashlib,json,os,re,struct,subprocess,sys
if os.name!='nt' or sys.argv[1:]!=['--approved-host-link-only']:
 raise SystemExit('Separate approval and Windows required')
ROOT=Path(__file__).resolve().parent
PINS=ROOT/'pins.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins=json.loads(PINS.read_text())
OUT=ROOT/'link-evidence-v1';OUT.mkdir(exist_ok=False)
receipt={'linked':False,'executed':False,'link_invocations':0,'pins_sha256':sha(PINS),'runner_sha256':sha(__file__)}
def save():(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
tracked=dict(pins['objects']);tracked.update(pins['libraries']);tracked.update(pins['tools'])
tracked[str(PINS)]=sha(PINS);tracked[str(Path(__file__).resolve())]=sha(__file__)
def verify():
 actual={p:sha(p) for p in tracked}
 if actual!=tracked:raise RuntimeError('Pinned input identity mismatch')
 return actual
def run(command,label):
 (OUT/(label+'-command.json')).write_text(json.dumps(command,indent=2)+'\n')
 try:p=subprocess.run(command,cwd=OUT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
 except subprocess.TimeoutExpired as e:
  (OUT/(label+'.log')).write_bytes(e.stdout or b'');raise
 (OUT/(label+'.log')).write_bytes(p.stdout)
 receipt[label+'_exit_code']=p.returncode;save()
 if p.returncode:raise RuntimeError(label+' failed; no retry')
 return p.stdout.decode(errors='replace')
try:
 (OUT/'before.json').write_text(json.dumps(verify(),indent=2)+'\n')
 if len(pins['objects'])!=18:raise RuntimeError('Expected exactly18 baseline host objects')
 for path in pins['objects']:
  if struct.unpack_from('<H',Path(path).read_bytes())[0]!=0x14c:raise RuntimeError('Non-x86 object')
 linker=next(p for p in pins['tools'] if p.lower().endswith('link.exe'))
 dumpbin=next(p for p in pins['tools'] if p.lower().endswith('dumpbin.exe'))
 executable=OUT/'paired-host74.exe'
 # Explicit allowlist and /NODEFAULTLIB prevent ambient library search or hidden replacements.
 command=[linker,'/NOLOGO','/WX','/MACHINE:X86','/SUBSYSTEM:CONSOLE','/INCREMENTAL:NO','/NODEFAULTLIB','/OPT:NOREF','/OPT:NOICF','/VERBOSE:LIB','/OUT:'+str(executable),'/MAP:'+str(OUT/'paired-host74.map')]+list(pins['objects'])+list(pins['libraries'])
 receipt['link_invocations']=1;save()
 run(command,'link')
 data=executable.read_bytes();offset=struct.unpack_from('<I',data,0x3c)[0]
 if data[:2]!=b'MZ' or data[offset:offset+4]!=b'PE\0\0' or struct.unpack_from('<H',data,offset+4)[0]!=0x14c:raise RuntimeError('Not an x86 PE')
 receipt['output_sha256']=sha(executable);receipt['output_bytes']=len(data)
 run([dumpbin,'/headers',str(executable)],'headers')
 imports=run([dumpbin,'/imports',str(executable)],'imports')
 observed=set(re.findall(r'\bAIL_\w+\b',imports));receipt['ail_import_names']=sorted(observed)
 if observed!=set(pins['expected_ail_names']):raise RuntimeError('Resolved AIL import set differs from actual18-object union')
 if 'mss32.dll' not in imports.lower():raise RuntimeError('Expected Miles DLL import absent')
 receipt['linked']=True
except Exception as e:receipt['failure']={'type':type(e).__name__,'message':str(e)}
finally:
 try:
  (OUT/'after.json').write_text(json.dumps(verify(),indent=2)+'\n');receipt['inputs_unchanged']=True
 except Exception as e:receipt['inputs_unchanged']=False;receipt['after_failure']=str(e)
 receipt['passed']=receipt['linked'] and receipt.get('inputs_unchanged',False) and not receipt.get('failure')
 save()
sys.exit(0 if receipt['passed'] else 1)
