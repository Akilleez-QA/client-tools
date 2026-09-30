# Prospective source-only fixtures; never invoke the native probe here.
from oracle import assess

def fixture(mode='idle',timing='after'):
 rows=[]
 def add(kind,arg=0,prior=0,thread=7,clock=None):
  rows.append([len(rows)+1,kind,arg,prior,thread,clock if clock is not None else 10*(len(rows)+1),123 if kind in [5,6] else 0])
 def reg(arg,prior):add(1,arg);add(2,arg,prior)
 if mode=='idle':
  for arg,prior in [(0,0),(1,0),(2,1),(0,2),(0,0),(2,0)]:reg(arg,prior)
 else:reg(1,0)
 add(3);add(4)
 if mode=='replace':
  if timing=='before':add(5,1,thread=8);reg(2,1)
  elif timing=='overlap':add(1,2);add(5,2,thread=8);add(2,2,1)
  else:reg(2,1);add(5,1,thread=8)
 elif mode=='active_null':
  add(5,1,thread=8);add(1,0,thread=10);add(2,0,1,thread=10);add(7,thread=9)
 else:add(5,2,thread=8)
 add(6,1 if mode=='active_null' or (mode=='replace' and timing!='overlap') else 2,thread=8)
 if mode!='active_null':reg(0,2)
 add(8);add(9)
 return 'META type=sample mode='+mode+' freq=1000 hold=100 watchdog=15000\nRESOURCE 123\n'+'\n'.join('R '+' '.join(map(str,x)) for x in rows)+'\nSUMMARY callbacks=1\n'

def mutate(text,kind,column,value):
 lines=text.splitlines();found=False
 for i,line in enumerate(lines):
  f=line.split()
  if not found and f[0]=='R' and int(f[2])==kind:f[column]=str(value);lines[i]=' '.join(f);found=True
 assert found
 changed='\n'.join(lines)+'\n';assert changed!=text
 return changed

valid=fixture();assert assess(valid)['selected']==2
assert assess(fixture('active_null'))['null_return_observation']=='before_release'
for timing in ['before','overlap','after']:
 assert assess(fixture('replace',timing))['selection_observation']==('overlap_or_equal' if timing=='overlap' else timing)
# Actual ambiguous equal timestamps on different threads are valid.
equal=mutate(fixture('replace','overlap'),5,6,50)
assert assess(equal)['selection_observation']=='overlap_or_equal'
negative={
 'zero_frequency':valid.replace('freq=1000','freq=0'),
 'malformed_extra_meta':valid+'META malformed\n',
 'unknown_kind':mutate(valid,5,2,99),
 'invalid_callback_label':mutate(valid,5,3,3),
 'start_return_before_start_clock':mutate(valid,4,6,1),
 'cleanup_before_start_return_clock':mutate(valid,8,6,1),
 'cleanup_end_before_begin_clock':mutate(valid,9,6,1),
 'cleanup_before_callback_last_work':mutate(valid,6,6,1000),
 'cleanup_before_registration_return':mutate(valid,2,6,1000),
 'same_thread_reversal':mutate(valid,6,6,1),
 'callback_before_start_clock':mutate(valid,5,6,1),
 'wrong_resource':valid.replace('RESOURCE 123','RESOURCE 124'),
 'wrong_prior_pointer':valid.replace('R 4 2 1 0','R 4 2 1 1'),
 'wrong_summary':valid.replace('callbacks=1','callbacks=2'),
 'sequence_gap':valid.replace('R 1 ','R 0 ',1),
}
for name,text in negative.items():
 assert text!=valid, name+' unchanged mutation'
 try:assess(text)
 except ValueError:continue
 raise AssertionError('negative accepted '+name)
print('PASS six valid classifications and fifteen changed negative fixtures; no native execution')
