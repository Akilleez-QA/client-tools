import hashlib,json,sys
from pathlib import Path
packet=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve()
native=packet/'native-text/pr-network18-v2-all'
export=json.loads((packet/'candidate-v2.tar.manifest.json').read_text())
identity=json.loads((native/'identity.json').read_text())
headers=json.loads((native/'included-files-sha256.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
checks.append(('native-reported-head',identity['reported_revision']==export['revision']))
for name,value in identity['sources'].items():
 checks.append(('source:'+name,sha(root/name)==value and export['files'][name]==value))
for path,value in headers.items():
 if path.startswith('checkout/'):
  rel=path[len('checkout/'):]
  # /showIncludes preserves forwarding paths' original spelling. Windows paths
  # are case insensitive; match the exact repository path through casefold.
  candidates=[name for name in export['files'] if name.casefold()==rel.casefold()]
  checks.append(('include:'+rel,len(candidates)==1 and export['files'][candidates[0]]==value and sha(root/candidates[0])==value))
 elif not (path.lower().startswith('c:\\program files (x86)\\microsoft visual studio 12.0\\') or path.lower().startswith('c:\\program files (x86)\\windows kits\\') or path.lower().startswith('c:\\pr-network18-v2-all\\')):
  checks.append(('unexpected-external-include:'+path,False))
checks.append(('runner-byte-identity',sha(root/'tools/test-windows-network-widths/run.py')==identity['runner_sha256']))
checks.append(('probe-byte-identity',sha(root/'tools/test-windows-network-widths/probe.cpp')==identity['probe_sha256']))
result={'passed':all(passed for _,passed in checks),'checks':len(checks),'failures':[name for name,passed in checks if not passed]}
(packet/'source-binding-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if result['passed'] else 1)
