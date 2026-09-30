"""Replay raw runtime output through the actual runner verdict block; no serializers mocked.
This is only a verdict/enforcement test. Runtime evidence is the separately compiled PE runs.
"""
import contextlib,io,json,pathlib,textwrap,types
root=pathlib.Path('/home/akilleez/Work/swg-source/client-login-wire-probe')
e=pathlib.Path(__file__).resolve().parent
source=(root/'tools/test-wire-compatibility/run.py').read_text()
block=source[source.index('        lines = run.stdout.splitlines()'):source.index('    finally:')]
ns={'EXPECTED_RUNTIME_PASSES':58,'EXPECTED_WIN64_ONLY_PASSES':7}
exec('def verdict(run, a, types_ok=True):\n'+textwrap.indent(textwrap.dedent(block),'    '),ns)
def output(name,bits):
 commands=[json.loads(s) for s in (e/name/f'commands-{bits}.jsonl').read_text().splitlines()]
 return commands[-1]['stdout']
def case(name,text,bits,required,want,exit=0):
 with contextlib.redirect_stdout(io.StringIO()) as capture:
  result=ns['verdict'](types.SimpleNamespace(stdout=text,returncode=exit),types.SimpleNamespace(bits=bits,require_current_coverage=required))
 print(f'{name}: verdict={result}, expected={want}; {capture.getvalue().strip()}')
 assert result==want,name
win32=output('candidate32',32);win64=output('candidate64',64);stock=output('oracle32',32)
case('candidate32',win32,32,True,0)
case('candidate64',win64,64,True,0)
case('stock32 known absence',stock,32,False,0)
case('stock32 current coverage rejects absence',stock,32,True,1)
case('missing login check',win64.replace('PASS: LoginClusterStatus empty literal decodes with exact consumption\n',''),64,True,1)
case('unknown absence',win64+'ABSENT: made-up all=3 win64=1\n',64,False,1)
case('malformed absence',win64+'ABSENT: malformed\n',64,False,1)
absent=next(s for s in stock.splitlines() if s.startswith('ABSENT:'))
case('duplicate known absence',stock+absent+'\n',32,False,1)
skip=next(s for s in win32.splitlines() if s.startswith('SKIP:'))
case('duplicate skip',win32+skip+'\n',32,True,1)
case('missing skip',win32.replace(skip+'\n',''),32,True,1)
case('spurious Win64 skip',win64+skip+'\n',64,True,1)
case('nonzero runtime exit',win64,64,True,1,exit=1)
case('explicit failure',win64+'FAIL: injected\n',64,True,1)
case('not run',win64+'NOT RUN: injected\n',64,True,1)
print('14/14 verdict cases passed (log replay only).')
