from pathlib import Path
import hashlib,json,struct
b=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log=(b/'native-hashes-cleanup.log').read_text().lower()
match={n:sha(b/n) in log for n in ['probe.cpp','probe.exe','Mss.h']};assert all(match.values())
pe={}
for n in ['probe.exe','private-prefix-cadence-a/drive_c/cadence-private/Mss32.dll']:
 data=(b/n).read_bytes();off=struct.unpack_from('<I',data,60)[0];assert data[off:off+4]==b'PE\0\0';pe[n]=hex(struct.unpack_from('<H',data,off+4)[0]);assert pe[n]=='0x14c'
(b/'identities.json').write_text(json.dumps(dict(native_transfer_matches=match,pe_machine=pe,native_scratch_removed='scratch_exists=false' in log),indent=2))
paths=[p for p in b.iterdir() if p.is_file() and p.name!='hashes.json']+list((b/'run-a').iterdir())
prefix=b/'private-prefix-cadence-a/drive_c'
paths+=list((prefix/'cadence-private').iterdir())
for d in ['windows/system32','windows/syswow64']:
 for n in ['ntdll.dll','kernel32.dll','winmm.dll','dsound.dll','mmdevapi.dll','winealsa.drv']:
  p=prefix/d/n
  if p.exists():paths.append(p)
for n in ['/usr/bin/wine','/usr/bin/wineserver','/usr/lib/alsa-lib/libasound_module_pcm_pulse.so']:
 p=Path(n)
 if p.exists():paths.append(p)
(b/'hashes.json').write_text(json.dumps({str(p):dict(bytes=p.stat().st_size,sha256=sha(p)) for p in paths if p.is_file()},indent=2))
print('native/local identities match; PE x86; manifest written')
