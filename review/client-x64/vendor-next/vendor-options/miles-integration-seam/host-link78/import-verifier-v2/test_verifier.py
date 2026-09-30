"""Prospective local text-only gate; no subprocess, PE or DLL access."""
from pathlib import Path
import hashlib,json
from verifier import verify
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
for name,digest in manifest['sha256'].items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Frozen input changed: '+name)
expected={'_AIL_startup@0','_AIL_open_digital_driver@16'}
valid='''    KERNEL32.dll
       01 CloseHandle
    MSS32.DLL
       0 Import Address Table
       0 Import Name Table
       0 time date stamp
       0 Index of first forwarder reference
       13C _AIL_startup@0
       081 _AIL_open_digital_driver@16
  Summary
'''
assert verify(valid,expected)==sorted(expected)
negative={
 'wrong_dll':valid.replace('MSS32.DLL','other.dll'),
 'missing':valid.replace('       13C _AIL_startup@0\n',''),
 'extra':valid.replace('  Summary','       99 _AIL_shutdown@0\n  Summary'),
 'wrong_stack_bytes':valid.replace('_AIL_open_digital_driver@16','_AIL_open_digital_driver@12'),
 'duplicate':valid.replace('  Summary','       13C _AIL_startup@0\n  Summary'),
 'undecorated':valid.replace('_AIL_startup@0','AIL_startup'),
 'also_wrong_group':valid.replace('       01 CloseHandle','       01 CloseHandle\n       13C _AIL_startup@0')}
for name,text in negative.items():
    try:verify(text,expected)
    except ValueError:continue
    raise AssertionError('False acceptance: '+name)
pins=json.loads((ROOT/'expected.json').read_text())
actual=verify((ROOT/'imports.log').read_text(),pins['decorated_names'],pins['dll'])
for name,digest in manifest['sha256'].items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Input changed during check')
print(json.dumps({'passed':True,'miniature_positive':1,'negative_fixtures':list(negative),'frozen_dump_matches':len(actual),'linked':False,'executed_target':False}))
