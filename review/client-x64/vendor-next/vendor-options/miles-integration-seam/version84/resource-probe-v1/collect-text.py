from pathlib import Path
import zipfile,json
b=Path(__file__).resolve().parent
names=['manifest.json','tool-identities.json']
for name in ['before.json','after.json','results.json']:
 if (b/'evidence-v1'/name).is_file():names.append('evidence-v1/'+name)
for stage in ['resource','compile','link','observation']:
 for suffix in ['.log','-command.json']:
  name='evidence-v1/'+stage+suffix
  if (b/name).is_file():names.append(name)
with zipfile.ZipFile(b/'curated-text.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in names:z.write(b/name,name)
print(json.dumps({'text_files':len(names),'private_environment_included':False,'binaries_included':False}))
