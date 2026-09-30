#!/usr/bin/env python3
"""Prospective one-attempt host49 gate. Must not execute before parent authorization."""
import hashlib, json, os, pathlib, re, subprocess, time
root=pathlib.Path(__file__).resolve().parent
frozen=json.loads((root/'freeze-v1.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for item in frozen['files']:
    if sha(root/item['path'])!=item['sha256']:raise SystemExit('Frozen input mismatch: '+item['path'])
evidence=root/'evidence-v1';evidence.mkdir(exist_ok=False)
binary=evidence/'host49-portable'
sources=['host-file-consumption49/file_tokens.cpp','host-file-consumption49/reply_transaction.cpp',
         'callback-protocol48/file_protocol.cpp','file-channel26/file_channel.cpp','transport-candidate/codec.cpp']
cmd=['/usr/bin/clang++','-std=c++11','-Wall','-Wextra','-Wpedantic','-Werror','-O1','-g',
     '-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer',
     str(root/'portable-v1/tests.cpp')]+[str(root/'candidate'/p) for p in sources]+['-o',str(binary)]
markers=[
 'PASS separate SDK token host registry and client wire identities with stale-token refusal',
 'PASS failed open publishes no token and non1 status stays exact',
 'PASS explicit and destructor presend cancellation permit slot reuse without token reuse',
 'PASS exact bounded read copy short read zero read and ACK result ordering',
 'PASS read buffer and remote target rejected before any send',
 'PASS signed seek bits preserved through real reply decoder',
 'PASS live capacity fails before another reservation and preserves output']
deaths=['issued','failed-context','failed-status','failed-read','failed-close','consumed-ack-uncertain']
env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1:abort_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1:print_stacktrace=1'
result={'scope':'real host49 token/consumption sources with real codec; no Endpoint/SDK/engine/native ABI',
        'first_attempt':True,'build_command':cmd,'sanitizers':{k:env[k] for k in ['ASAN_OPTIONS','UBSAN_OPTIONS']},
        'start_epoch':time.time(),'build_exit':None,'positive_exit':None,'deaths':[]}
(evidence/'commands.json').write_text(json.dumps({'build':cmd,'positive':[str(binary)],'death_commands':[[str(binary),d] for d in deaths]},indent=2)+'\n')
try:
    with (evidence/'build.log').open('wb') as out:
        result['build_exit']=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,timeout=120).returncode
    if result['build_exit']==0:
        with (evidence/'positive.log').open('wb') as out:
            result['positive_exit']=subprocess.run([str(binary)],env=env,stdout=out,stderr=subprocess.STDOUT,timeout=30).returncode
        text=(evidence/'positive.log').read_text(errors='replace');lines=text.splitlines()
        result['scenario_counts']={marker:lines.count(marker) for marker in markers}
        counts=re.findall(r'^PASS ([0-9]+) positive host49 checks; no Endpoint SDK or engine$',text,re.M)
        result['positive_checks']=int(counts[0]) if len(counts)==1 else None
        result['positive_pass']=(result['positive_exit']==0 and len(counts)==1 and all(n==1 for n in result['scenario_counts'].values()))
        if result['positive_pass']:
            for mode in deaths:
                with (evidence/('death-'+mode+'.log')).open('wb') as out:
                    code=subprocess.run([str(binary),mode],env=env,stdout=out,stderr=subprocess.STDOUT,timeout=15).returncode
                text=(evidence/('death-'+mode+'.log')).read_text(errors='replace')
                match=re.fullmatch(r'EXPECTED_TERMINATE '+re.escape(mode)+r' checks=([0-9]+)\n',text)
                entry={'mode':mode,'exit':code,'expected_exit':73,'armed_oracle_checks':int(match.group(1)) if match else None,
                       'pass':code==73 and match is not None,
                       'scope':'expected production destructor std::terminate only; _Exit deliberately skips teardown/leak analysis'}
                result['deaths'].append(entry)
                if not entry['pass']:break # Preserve first failure; no retries or remaining death probes.
except Exception as exc:result['error']=repr(exc)
finally:
    result['frozen_inputs_changed']=[x['path'] for x in frozen['files'] if not (root/x['path']).is_file() or sha(root/x['path'])!=x['sha256']]
    result['end_epoch']=time.time()
    result['pass']=(result['build_exit']==0 and result.get('positive_pass',False) and
                    len(result['deaths'])==len(deaths) and all(d['pass'] for d in result['deaths']) and
                    not result['frozen_inputs_changed'])
    (evidence/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));raise SystemExit(0 if result['pass'] else 1)
