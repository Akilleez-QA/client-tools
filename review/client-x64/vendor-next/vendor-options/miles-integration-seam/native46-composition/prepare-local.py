from pathlib import Path
import hashlib,json,shutil
D=Path(__file__).resolve().parent;B=D.parent;SOURCE=B/'callback-composition46/candidate';OUT=D/'private-inputs-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
OUT.mkdir(exist_ok=False)
production=['callback-control45/host_association_mapper.h','callback-control45/host_association_mapper.cpp','native-file-callbacks35/ClientMilesFileCallbacks.h','reverse-file-seam20/ClientAudioFileCallbacks.h','selected-file-services44/selected_services.h','selected-file-services44/selected_services.cpp','file-owner36/session_file_owner.h','file-owner36/session_file_owner.cpp','file-channel26/file_channel.h','file-channel26/file_channel.cpp','file-executor33/EngineFileWorker.h','file-executor33/FileInvocationJob.h','file-executor33/FileInvocationJob.cpp','protocol-candidate/miles_wire.h','transport-candidate/codec.h','transport-candidate/codec.cpp','transport-candidate/resource_registry.h','session-file-admission34/coordinator.h','session-file-admission34/coordinator.cpp']
for n in production:
 p=OUT/'candidate'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SOURCE/n,p)
# No portable fixture, fake windows header, test callback or compatibility macro.
prior=B/'native41-owner/native-evidence-v1/curated'
r=json.loads((prior/'results/results.json').read_text());reuse={'origin':'native41-owner codec/coordinator only','sha256':{},'objects':{},'source_dependencies':{},'tool_sha256':r['tools']}
for unit in ['codec','coordinator']:
 row=next(x for x in r['builds'] if x['unit']==unit);base='C:/native41-owner/results/'+unit+'/'
 reuse['objects'][base+unit+'.obj']={'sha256':row['object_sha256'],'machine':'0x8664'};reuse['sha256'][base+unit+'.obj']=row['object_sha256']
 reuse['sha256']['C:/native41-owner/candidate/'+row['source']]=sha(SOURCE/row['source'])
 assert sha(SOURCE/row['source'])==sha(B/'native41-owner/private-inputs-v1/candidate'/row['source'])
 for n in ['command.json','compile.log','actual-includes.json','symbols.log','symbols-command.json']:
  reuse['sha256'][base+n]=sha(prior/'results'/unit/n)
 includes=json.loads((prior/'results'/unit/'actual-includes.json').read_text())
 for path,value in includes.items():
  normalized=path.replace('\\','/');prefix='C:/native41-owner/candidate/'
  if normalized.lower().startswith(prefix.lower()):
   relative=normalized[len(prefix):]
   assert sha(SOURCE/relative)==value,relative
   reuse['source_dependencies'][relative]=value;reuse['sha256'][path]=value
reuse['sha256'].update(r['tools']);(OUT/'reused-units.json').write_text(json.dumps(reuse,indent=2)+'\n')
for n in ['flags.json','require-v120.h']:shutil.copy2(B/'native41-owner/private-inputs-v1'/n,OUT/n)
for n in ['run-native.py','symbol_parser.py']:shutil.copy2(D/n,OUT/n)
entries={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file()}
(OUT/'input-manifest.json').write_text(json.dumps({'sha256':entries},indent=2)+'\n')
print(json.dumps({'count':len(entries),'manifest':sha(OUT/'input-manifest.json'),'runner':sha(D/'run-native.py')},indent=2))
