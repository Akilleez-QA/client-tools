"""Authored-only parser/table checks. No VM, SDK, subprocess or vendor execution."""
from pathlib import Path
import ast
import importlib.util
import json
import re
BASE = Path(__file__).resolve().parent
for path in BASE.glob('*.py'):
    ast.parse(path.read_text())
table = json.loads((BASE / 'sequence.json').read_text())
triples = re.findall(r'\{(\d+), (\d+), (\d+)\}', (BASE / 'sequence.h').read_text())
assert [[r['opcode'], r['admission'], r['status']] for r in table] == [list(map(int,t)) for t in triples]
spec = importlib.util.spec_from_file_location('runner27', BASE / 'run-live27.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
controller = []
host = []
for row in table:
    i = row['request']
    text = '372e326100' if i == 2 else '-'
    size = 5 if i == 2 else 0
    value = 1 if i == 4 else 2 if i == 12 else 0
    controller.append('reply request=%d opcode=%d status=%d bytes=%d sha256=%s return_bits=%d value3=%d null_mask=0 text_hex=%s' %
                      (i,row['opcode'],row['status'],128+size,'a'*64,value,2 if i==6 else 0,text))
    host.append('request=%d opcode=%d admission=%d transport=%d vendor=%d text_bytes=%d' %
                (i,row['opcode'],row['admission'],row['status'],value,size))
host.append('original_room=0')
for i, fields in [(7,[('position.x','bfa00000'),('position.y','40200000'),('position.z','c0700000')]),
                  (8,[('velocity.x','3a83126f'),('velocity.y','bb03126f'),('velocity.z','3b449ba6')]),
                  (9,[('face.x','3f800000'),('face.y','00000000'),('face.z','00000000'),('up.x','00000000'),('up.y','3f800000'),('up.z','00000000')]),
                  (10,[('rolloff','3f000000')]),
                  (16,[('position.x','bfa00000'),('position.y','40200000'),('position.z','c0700000')])]:
    for field, bits in fields:
        host.append('state request=%d field=%s actual=%s expected=%s'%(i,field,bits,bits))
for i,value in [(11,2),(12,2),(13,0),(14,0),(19,0)]:
    host.append('room request=%d actual=%d expected=%d'%(i,value,value))
host += ['idle_serve_returned request=15','PASS host27 ordered shutdown; retained directory bytes=6']
controller.append('PASS pipe-live27 exact22; seven operations; no playback/callbacks')
c,h='\n'.join(controller),'\n'.join(host)
runner.parse_trace(c,h)
mutations=[(c,h.replace('original_room=0','original_room=2')),
           (c,h.replace('room request=11 actual=2','room request=11 actual=0')),
           (c,h.replace('actual=3a83126f','actual=3a831270')),
           (c,h.replace('admission=15 transport=2','admission=16 transport=2',1)),
           (c.replace('request=21 opcode=26 status=4097','request=21 opcode=26 status=0'),h),
           (c,h+'\nFAIL emergency vendor cleanup'),
           (c.replace(controller[0]+'\n',''),h)]
for badc,badh in mutations:
    try: runner.parse_trace(badc,badh)
    except RuntimeError: pass
    else: raise AssertionError('negative trace accepted')
print('PASS authored source syntax,22 table, synthetic parser positive and7 negative controls; no native/vendor evidence')
