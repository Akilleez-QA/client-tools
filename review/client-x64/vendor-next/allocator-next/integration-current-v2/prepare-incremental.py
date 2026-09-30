from pathlib import Path
import subprocess,tarfile,io,json,hashlib,time,sys
root=Path('/home/akilleez/Work/swg-source/client-build-next');out=Path(__file__).resolve().parent/'incremental-v3-input';out.mkdir(exist_ok=False)
base='94a81438c4c442f21105a58047c82d34e04c9cb4';head=subprocess.check_output(['git','rev-parse',sys.argv[1]],cwd=root,text=True).strip()
paths=subprocess.check_output(['git','diff','--name-only','-z',base,head],cwd=root).decode().strip('\0').split('\0');existing=set(subprocess.check_output(['git','ls-tree','-rz','--name-only',head],cwd=root).decode().strip('\0').split('\0'));rows=[];deleted=[]
with tarfile.open(out/'overlay.tar','w') as t:
 for p in paths:
  if p not in existing:deleted.append(p);continue
  data=subprocess.check_output(['git','show',head+':'+p],cwd=root);i=tarfile.TarInfo(p);i.size=len(data);i.mode=0o644;i.mtime=int(time.time());t.addfile(i,io.BytesIO(data));rows.append({'path':p,'sha256':hashlib.sha256(data).hexdigest()})
(out/'manifest.json').write_text(json.dumps({'base':base,'head':head,'files':rows,'deleted':deleted},indent=2));(out/'changes.patch').write_bytes(subprocess.check_output(['git','diff','--binary',base,head],cwd=root));print(head,len(rows),'files',len(deleted),'deletions')
