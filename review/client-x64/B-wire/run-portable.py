import os, pathlib, runpy, subprocess, sys
from unittest.mock import patch
runner=pathlib.Path(sys.argv[1]); args=sys.argv[2:]; original=subprocess.run
def run(command, **kwargs):
 if command[0]=='wine':
  kwargs['env']=dict(kwargs['env'],WINEARCH='win64',WINEPREFIX=os.environ['SWG_TEST_WINEPREFIX'])
 result=original(command,**kwargs)
 if '-fsyntax-only' in command: print('SYNTAX EXIT:',result.returncode,flush=True)
 return result
sys.argv=[str(runner),*args]
with patch('subprocess.run',run):runpy.run_path(str(runner),run_name='__main__')
