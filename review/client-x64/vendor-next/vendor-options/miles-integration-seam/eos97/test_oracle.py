# Prospective pure fixtures only; this file has not been executed.
from oracle import assess

def fixture(mode='idle',which=2,entry=80):
 events=[]
 def add(kind,arg=0,prior=0,clock=None):events.append([len(events)+1,kind,arg,prior,7,clock if clock is not None else (len(events)+1)*10,123 if kind in [5,6] else 0])
 def reg(arg,prior):add(1,arg);add(2,arg,prior)
 if mode=='idle':
  for arg,old in [(0,0),(1,0),(2,1),(0,2),(0,0),(2,0)]:reg(arg,old)
 else:reg(1,0)
 add(3);add(4)
 if mode=='replace':
  if entry<50:
   add(5,which,clock=entry);add(1,2,clock=50);add(2,2,1,clock=60)
  elif entry<=60:
   add(1,2,clock=50);add(5,which,clock=entry);add(2,2,1,clock=60)
  else:
   add(1,2,clock=50);add(2,2,1,clock=60);add(5,which,clock=entry)
 else:add(5,which,clock=entry)
 if mode=='active_null':reg(0,1);add(7)
 add(6,which,clock=max(entry+1,len(events)*10+10))
 if mode!='active_null':reg(0,2)
 add(8);add(9)
 return 'META type=sample mode='+mode+' freq=1000 hold=100 watchdog=15000\nRESOURCE 123\n'+'\n'.join('R '+' '.join(map(str,x)) for x in events)+'\nSUMMARY callbacks=1\n'
valid=fixture();assert assess(valid)['selected']==2
assert assess(fixture('active_null',1))['quiescence_proven'] is False
assert assess(fixture('replace',1,100))['selection_observation']=='after'
assert assess(fixture('replace',2,55))['selection_observation']=='overlap_or_equal'
assert assess(fixture('replace',1,45))['selection_observation']=='before'
negative=[valid.replace('R 4 2 1 0','R 4 2 1 1'),valid.replace('SUMMARY callbacks=1','SUMMARY callbacks=2'),valid.replace('RESOURCE 123','RESOURCE 124'),valid.replace('hold=100','hold=200'),valid.replace('R 1 ','R 0 ',1),valid.replace('R 15 5 2','R 15 5 1'),valid.replace('R 20 9','R 20 8')]
for i,text in enumerate(negative):
 try:assess(text)
 except ValueError:continue
 raise AssertionError('negative accepted '+str(i))
print('PASS five valid classifications and seven negative fixtures; no runtime inference')
