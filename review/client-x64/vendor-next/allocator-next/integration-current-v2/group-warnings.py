from pathlib import Path
from collections import Counter
import re,json,hashlib,posixpath
base=Path(__file__).resolve().parent;rows={};counts={};unparsed=[]
pattern=re.compile(r'(?:^|>)([^>]+?)\((\d+)(?:,\d+)?\): warning (C\d+): (.*?)(?: \[(.*?)\])?$')
for cfg in ['Release','Debug']:
 p=base/'results'/(cfg+'-x64.log');raw=p.read_text(errors='replace');count=0
 for line in raw.splitlines():
  if ': warning ' not in line:continue
  count+=1;m=pattern.search(line.strip())
  if not m:unparsed.append(dict(config=cfg,line=line));continue
  path=m[1].strip().replace('\\','/').lower();path=path.split('/repo/')[-1]
  if not path.startswith('src/') and m[5]:
   project=m[5].replace('\\','/').lower().split('/repo/')[-1];path=posixpath.normpath(posixpath.join(posixpath.dirname(project),path))
  key=(path,int(m[2]),m[3]);r=rows.setdefault(key,dict(file=path,line=int(m[2]),code=m[3],occurrences=0,configs=[],messages=[],projects=[]));r['occurrences']+=1
  for field,value in [('configs',cfg),('messages',m[4]),('projects',m[5])]:
   if value and value not in r[field]:r[field].append(value)
 counts[cfg]=dict(raw_warning_lines=count,log_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
result=dict(counts=counts,unique_locations=len(rows),by_code=dict(Counter(r['code'] for r in rows.values())),unparsed=unparsed,warnings=sorted(rows.values(),key=lambda r:(r['code'],r['file'],r['line'])))
(base/'warnings-grouped.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['warnings','unparsed']},indent=2));print('unparsed',len(unparsed))
for r in result['warnings']:
 if r['code'] in ['C4311','C4312','C4302'] or any('pointer' in x.lower() or 'allocation' in x.lower() for x in r['messages']):print(r['file'],r['line'],r['code'],r['messages'][0])
