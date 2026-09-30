from pathlib import Path
b=Path(__file__).resolve().parent
s=(b.parent/'miles-rpc-contract/run.py').read_text()
s=s.replace("'private-prefix-rpc-b'","'private-prefix-generation'").replace("out=base/'run-b'","out=base/'rawlogs'").replace("'swg_rpc_'","'swg_gen_'").replace('rpc-private','generation-private')
s=s.replace("for label in [f'{route}-{mode}-{n}' for mode in ['sample','stream'] for route in ['direct','controlled'] for n in range(1,3)]:\n  route,mode,_=label.split('-')", "for label in [f'{route}-{mode}' for mode in ['sample','stream'] for route in ['direct','controlled','mutant']]:\n  route,mode=label.split('-')")
s=s.replace("'C:\\\\generation-private\\\\sample.wav',mode]);commands.append(cmd)","'C:\\\\generation-private\\\\sample.wav',mode,'mutant' if route=='mutant' else 'controlled']);commands.append(cmd)")
s=s.replace("assert rec['returncode']==0 and not rec.get('timed_out'),rec", "assert rec['returncode']==(9 if route=='mutant' else 0) and not rec.get('timed_out'),rec")
s=s.replace("result['private_wineserver_stop']=subprocess.run(['wineserver','-k'],env=env,timeout=10).returncode", "result['private_wineserver_stop']=subprocess.run(['wineserver','-k'],env=env,timeout=10).returncode\n  result['private_wineserver_wait']=subprocess.run(['wineserver','-w'],env=env,timeout=10).returncode")
(b/'run.py').write_text(s)
