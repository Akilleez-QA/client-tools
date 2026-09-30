"""Pure log classification; no process/audio/vendor operations."""
import re

def assess(text):
 lines=text.splitlines();meta=[];handles=[];records=[];summaries=[]
 for line in lines:
  if not line.strip():continue
  m=re.fullmatch(r'META type=(sample|stream) mode=(idle|replace|active_null) freq=(\d+) hold=100 watchdog=15000',line)
  if m:meta.append(m);continue
  m=re.fullmatch(r'RESOURCE (\d+)',line)
  if m:handles.append(int(m.group(1)));continue
  m=re.fullmatch(r'R (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)',line)
  if m:records.append(tuple(map(int,m.groups())));continue
  m=re.fullmatch(r'SUMMARY callbacks=(\d+)',line)
  if m:summaries.append(int(m.group(1)));continue
  raise ValueError('unrecognized or malformed line')
 if len(meta)!=1 or int(meta[0].group(3))<=0:raise ValueError('metadata/frequency')
 mode=meta[0].group(2)
 if len(handles)!=1 or not handles[0]:raise ValueError('resource')
 if summaries!=[1]:raise ValueError('summary')
 if [x[0] for x in records]!=list(range(1,len(records)+1)):raise ValueError('sequence')
 clocks={}
 for seq,kind,arg,prior,thread,clock,resource in records:
  if kind not in range(1,10) or not thread:raise ValueError('kind/thread')
  if clock<clocks.get(thread,0):raise ValueError('same-thread clock reversal')
  clocks[thread]=clock
  if kind in [1,2]:
   if arg not in [0,1,2] or prior not in [0,1,2,3] or (kind==1 and prior):raise ValueError('registration label')
  elif kind in [5,6]:
   if arg not in [1,2] or prior:raise ValueError('callback label')
  elif arg or prior:raise ValueError('unexpected event arguments')
  if (kind in [5,6] and resource!=handles[0]) or (kind not in [5,6] and resource):raise ValueError('resource label')
 by=lambda kind:[x for x in records if x[1]==kind]
 if len(by(3))!=1 or len(by(4))!=1 or len(by(8))!=1 or len(by(9))!=1:raise ValueError('one playback/cleanup')
 entries=by(5);exits=by(6)
 if len(entries)!=1 or len(exits)!=1 or entries[0][2]!=exits[0][2] or entries[0][6]!=handles[0] or exits[0][6]!=handles[0]:raise ValueError('callback identity/count')
 if entries[0][0]>=exits[0][0]:raise ValueError('callback order')
 begins=by(1);ends=by(2)
 if len(begins)!=len(ends):raise ValueError('unreturned registration')
 # Scripts issue no simultaneous registrations; pair by ordinal, never current callback shadow.
 for begin,end in zip(begins,ends):
  if begin[2]!=end[2] or begin[0]>=end[0]:raise ValueError('registration pairing')
 wanted=[0,1,2,0,0,2,0] if mode=='idle' else [1,2,0] if mode=='replace' else [1,0]
 if [x[2] for x in ends]!=wanted:raise ValueError('registration script')
 prior=[x[3] for x in ends]
 if mode=='idle':
  if prior[1:]!=[0,1,2,0,0,2] or entries[0][2]!=2:raise ValueError('idle prior/selection')
 else:
  if prior[1:]!=([1,2] if mode=='replace' else [1]):raise ValueError('prior pointer')
  if mode=='active_null' and entries[0][2]!=1:raise ValueError('active callback')
 # Slot order is not a universal cross-thread clock order. Check only actual
 # script happens-before edges; equal QPC ticks remain allowed.
 def before(a,b):
  if a[0]>=b[0] or a[5]>b[5]:raise ValueError('causal barrier')
 start=by(3)[0];returned=by(4)[0];cleanup=by(8)[0];cleaned=by(9)[0]
 before(start,returned);before(returned,cleanup);before(cleanup,cleaned)
 before(start,entries[0]);before(entries[0],exits[0]);before(exits[0],cleanup)
 for a,z in zip(begins,ends):before(a,z);before(z,cleanup)
 if mode=='idle':
  before(ends[5],start);before(exits[0],begins[6])
 elif mode=='replace':
  before(ends[0],start);before(returned,begins[1]);before(exits[0],begins[2])
 else:
  before(ends[0],start);before(entries[0],begins[1])
 release=by(7)
 if mode!='active_null' and release:raise ValueError('unexpected hold release')
 if mode=='active_null':
  if len(release)!=1:raise ValueError('hold count')
  before(entries[0],release[0]);before(release[0],exits[0]);before(release[0],cleanup)
 result={'mode':mode,'prior_initial':prior[0],'selected':entries[0][2],'quiescence_proven':False}
 if mode=='replace':
  t=entries[0][5];a=begins[1][5];b=ends[1][5]
  result['selection_observation']='before' if t<a else 'after' if t>b else 'overlap_or_equal'
 if mode=='active_null':
  release=by(7)
  if len(release)!=1 or not(entries[0][0]<release[0][0]<exits[0][0]):raise ValueError('hold barrier')
  result['null_return_observation']='before_release' if ends[1][5]<release[0][5] else 'after_release' if ends[1][5]>release[0][5] else 'equal_ambiguous'
 return result
