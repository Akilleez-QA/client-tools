from pathlib import Path
import hashlib,json,shutil,subprocess
D=Path(__file__).resolve().parent;B=D.parent;P=D/'private-inputs-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=B/'file-owner37';m=json.loads((old/'candidate-manifest-v1.json').read_text())
for n,v in m['sha256'].items():assert sha(old/n)==v,n
product=Path('/home/akilleez/Work/swg-source/client-build-next')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=product,text=True).strip()=='49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=product)
P.mkdir(exist_ok=False)
for f in (old/'candidate').rglob('*'):
 if f.is_file() and f.name not in ['portable_job.cpp','tests.cpp','test_allocators.cpp','test_allocators.h']:
  dest=P/'candidate'/f.relative_to(old/'candidate');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
for n in ['call_context.h','call_context.cpp']:
 p=P/'candidate/host-callback-context41'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(B/'host-callback-context41'/n,p)
# Original engine worker source is not compiled. Pin prior proven source identity only.
assert sha(P/'candidate/file-executor33/EngineFileWorker.h')==sha(B/'file-executor33/EngineFileWorker.h')
assert sha(P/'candidate/file-executor33/FileInvocationJob.cpp')==sha(B/'file-executor33/FileInvocationJob.cpp')
flags=['/nologo','/c','/EHsc','/Y-','/Gm-','/Zc:wchar_t-','/Zc:forScope','/GR','/Gy','/fp:precise','/W4','/Zi','/FC','/showIncludes','/MTd','/Od','/Ob1','/RTC1','/WX','/DWIN32','/D_DEBUG','/D_MBCS','/DDEBUG_LEVEL=2','/D_CRT_SECURE_NO_DEPRECATE=1','/D_LIB']
(P/'flags.json').write_text(json.dumps(flags,indent=2)+'\n')
(P/'require-v120.h').write_text('#if !defined(_MSC_VER) || _MSC_VER != 1800 || !defined(_WIN64)\n#error Requires actual v120 AMD64 object test\n#endif\n')
shutil.copy2(D/'run-native.py',P/'run-native.py')
entries={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file()}
(P/'input-manifest.json').write_text(json.dumps({'sha256':entries},indent=2)+'\n')
print(json.dumps({'entries':len(entries),'input_manifest':sha(P/'input-manifest.json'),'runner':sha(D/'run-native.py'),'unchanged_worker_cpp':sha(B/'file-executor33/EngineFileWorker.cpp'),'worker_header':sha(B/'file-executor33/EngineFileWorker.h')},indent=2))
