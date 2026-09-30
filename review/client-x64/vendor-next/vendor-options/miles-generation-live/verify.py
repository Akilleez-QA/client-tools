"""Postprocessing checks only; never launches playback."""
import subprocess,sys,json
from pathlib import Path
from analyze import eos_context
b=Path(__file__).resolve().parent
pairs={8:[{'qpc':100},{'qpc':110}],9:[{'qpc':200},{'qpc':210}]}
e=dict(observed_last_id=8,observed_last_op=5,active_id=0,active_op=0,qpc=150)
assert eos_context(e,pairs)=='BETWEEN'  # outside last command window: legal
try:eos_context(dict(e,active_id=8,active_op=5),pairs)
except AssertionError:pass
else:raise AssertionError('incorrect active-window attribution accepted')
assert eos_context(dict(e,active_id=8,active_op=5,qpc=105),pairs)=='ACTIVE'
try:eos_context(dict(e,qpc=220),pairs)
except AssertionError:pass
else:raise AssertionError('incorrect observed last command accepted')
result={'eos_cases':{'between_outside_last_window':'accepted','active_outside_window':'rejected','active_inside_window':'accepted','wrong_last_command':'rejected'},'validators':[]}
for label in [f'{route}-{mode}' for mode in ['sample','stream'] for route in ['direct','controlled','mutant']]:
 r=subprocess.run([sys.executable,str(b/'analyze.py'),'--validate',str(b/'rawlogs'/(label+'.log'))],capture_output=True,text=True)
 (b/(label+'-validation.json')).write_text(r.stdout)
 assert not r.stderr,r.stderr
 assert r.returncode==(1 if label.startswith('mutant') else 0)
 result['validators'].append(dict(label=label,returncode=r.returncode))
(b/'postprocessing-checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
