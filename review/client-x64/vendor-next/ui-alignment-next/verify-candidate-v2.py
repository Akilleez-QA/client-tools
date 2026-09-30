from pathlib import Path
import json,re,subprocess
root=Path('C:/ui-alignment-candidate-v2');results=json.loads((root/'results.json').read_text())
for r in results:
 d=root/r['name'];assert r['compile']==0
 p=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(d/'run-verified.log').write_bytes(p.stdout)
 lines=p.stdout.decode(errors='replace').splitlines();expected='PASS: 3129 UI alignment checks'
 extras=[x for x in lines if x!=expected]
 okay=p.returncode==0 and lines.count(expected)==1 and all(re.fullmatch(r'MM::remove \d+/\d+=bytes \d+/\d+=allocs',x) for x in extras)
 if r['name'].startswith('Release'):okay=okay and not extras
 mapping=(d/'probe.map').read_text(errors='replace');binding=any('?allocMem@UiMemoryBlockManager@@' in x and '0.obj' in x for x in mapping.splitlines())
 r.update(verified_exit=p.returncode,verified_pass=okay and binding,production_map_binding=binding,diagnostic_lines=extras)
(root/'verified-results.json').write_text(json.dumps(results,indent=2));print([(r['name'],r['verified_pass']) for r in results]);raise SystemExit(0 if all(r['verified_pass'] for r in results) else 1)
