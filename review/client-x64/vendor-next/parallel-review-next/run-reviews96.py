from pathlib import Path
import json,hashlib,subprocess,signal,concurrent.futures,time
r=Path(__file__).resolve().parent;b=r.parent/'vendor-options/miles-integration-seam'
def sha(v):return hashlib.sha256(v).hexdigest()
def run(name,model,intro,paths):
 inputs={};prompt=intro+'\nUse only supplied authored source; do not run tools, change files, consult other reviews, or infer vendor behavior. Return concrete source-grounded concerns and scope limits; no broad clearance.\n'
 for path in paths:
  data=path.read_bytes();inputs[str(path)]=sha(data);prompt+='\nFILE '+str(path.relative_to(b))+'\n'+data.decode()
 (r/(name+'-prompt.txt')).write_text(prompt)
 meta={'model':model,'prompt_sha256':sha(prompt.encode()),'prompt_bytes':len(prompt.encode()),'inputs':inputs,'timeout_seconds':240,'retry':False}
 (r/(name+'-identity.json')).write_text(json.dumps(meta,indent=2)+'\n')
 start=time.time()
 with (r/(name+'-log.txt')).open('wb') as f:
  proc=subprocess.Popen(['cursor-agent','--print','--mode','ask','--sandbox','enabled','--trust','--model',model,'--workspace',str(r),prompt],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  try:rc=proc.wait(timeout=240)
  except subprocess.TimeoutExpired:oskill=signal.SIGKILL;__import__('os').killpg(proc.pid,oskill);proc.wait();rc=124
 (r/(name+'-exit.txt')).write_text(str(rc)+'\n'); data=(r/(name+'-log.txt')).read_bytes();meta.update(exit_code=rc,elapsed_seconds=round(time.time()-start,2),log_bytes=len(data),log_sha256=sha(data))
 (r/(name+'-identity.json')).write_text(json.dumps(meta,indent=2)+'\n');return {'name':name,**meta}

jobs=[('composer-version96','composer-2.5','Blind source/test review of native-shaped MSS_version portable adapter. Find concrete mismatches or falsepasses. Scope is accepted positive capacities up to explicit reply budget; native adapter has no pipe cap. Examine exact capacity forwarding, reply ownership and destination nonmutation. No native execution inference.',[b/'version90/from86.patch',b/'version92/tests.cpp',b/'version92/PLAN.md']),('grok-version96','grok-4.7-medium','Independent narrow review of Windows version resource wrapper in an x86 helper behind native-shaped API. Actual own-resource observation: LoadStringA on recorded Win32 ACP1252 for capacities1,2,4,6,7,11 writes truncated prefix plus NUL, including zero for empty/missing IDs. This is not universal vendor/codepage evidence. Review capacity and exact output-byte copying, integer conversions, module lifetime and cleanup. Explicit limitations include max1048448 and unsupported no-NUL API outcome. Identify concrete C++ defects or semantic mismatches within scope; distinguish unsupported external cases. No broad clearance.',[b/'version90/candidate/session-version22/session_version_host.cpp',b/'version90/candidate/session-version22/session_version.cpp',b/'version90/candidate/startup-bridge23/reply.h'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for result in ex.map(lambda args:run(*args),jobs):
  print(json.dumps({k:result[k] for k in ['name','model','exit_code','elapsed_seconds','log_bytes','log_sha256']}),flush=True)
