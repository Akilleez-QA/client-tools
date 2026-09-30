"""Pure log classification; no process/audio/vendor operations."""
import re

def assess(text):
 lines=text.splitlines();meta=[re.fullmatch(r'META type=(sample|stream) mode=(idle|replace|active_null) freq=(\d+) hold=100 watchdog=15000',x) for x in lines if x.startswith('META ')];meta=[x for x in meta if x]
 if len(meta)!=1:raise ValueError('metadata')
 mode=meta[0].group(2)
 handles=[int(x.split()[1]) for x in lines if re.fullmatch(r'RESOURCE \d+',x)]
 if len(handles)!=1 or not handles[0]:raise ValueError('resource')
 records=[]
 for line in lines:
  if line.startswith('R '):
   fields=line.split()
   if len(fields)!=8:raise ValueError('record shape')
   records.append(tuple(map(int,fields[1:])))
 if [x[0] for x in records]!=list(range(1,len(records)+1)):raise ValueError('sequence')
 by=lambda kind:[x for x in records if x[1]==kind]
 if len(by(3))!=1 or len(by(4))!=1 or len(by(8))!=1 or len(by(9))!=1:raise ValueError('one playback/cleanup')
 entries=by(5);exits=by(6)
 if len(entries)!=1 or len(exits)!=1 or entries[0][2]!=exits[0][2] or entries[0][6]!=handles[0] or exits[0][6]!=handles[0]:raise ValueError('callback identity/count')
 if entries[0][0]>=exits[0][0]:raise ValueError('callback order')
 if lines.count('SUMMARY callbacks=1')!=1:raise ValueError('summary')
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
 result={'mode':mode,'prior_initial':prior[0],'selected':entries[0][2],'quiescence_proven':False}
 if mode=='replace':
  t=entries[0][5];a=begins[1][5];b=ends[1][5]
  result['selection_observation']='before' if t<a else 'after' if t>b else 'overlap_or_equal'
 if mode=='active_null':
  release=by(7)
  if len(release)!=1 or not(entries[0][0]<release[0][0]<exits[0][0]):raise ValueError('hold barrier')
  result['null_return_observation']='before_release' if ends[1][5]<release[0][5] else 'after_release' if ends[1][5]>release[0][5] else 'equal_ambiguous'
 return result
