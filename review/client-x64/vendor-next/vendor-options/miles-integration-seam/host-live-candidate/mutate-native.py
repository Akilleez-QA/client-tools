from pathlib import Path
import subprocess
r=Path('C:/miles-host-live-mutant-v1');p=r/'host-candidate/host_dispatch.cpp';s=p.read_text();old='::AIL_set_sample_volume_levels(sample,f(call.value[0]),f(call.value[1]));';assert s.count(old)==1;p.write_text(s.replace(old,'::AIL_set_sample_volume_levels(sample,f(call.value[1]),f(call.value[0]));'))
p=r/'host-live-candidate/build-native.py';p.write_text(p.read_text().replace('miles-host-live-v3','miles-host-live-mutant-v1'))
raise SystemExit(subprocess.run(['C:/ci-dpvs-review/python/python.exe',str(p)]).returncode)
