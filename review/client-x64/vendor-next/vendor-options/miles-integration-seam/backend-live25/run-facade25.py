"""One pending, separately authorized facade25 live gate; never retry a failed run."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import uuid

BASE = Path(__file__).resolve().parent
DLL_SHA256 = '0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
OPERATIONS = [4096, 4101, 34, 34, 34, 56, 10, 10, 12, 12, 33, 10, 33, 10, 33,
              10, 14, 53, 53, 53, 52, 10, 4109]
STATUSES = {5: 3, 15: 3, 18: 3, 19: 2, 22: 4097}
ADMISSIONS = list(range(18)) + [17, 18, 19, 19, 20]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def call(*arguments):
    return subprocess.check_output(arguments, text=True, timeout=15).strip()


def plugin_hashes(directory):
    return {str(path.relative_to(directory)): digest(path)
            for path in sorted(directory.rglob('*')) if path.is_file()}


def parse_trace(controller, host):
    pattern = (r'^reply request=(\d+) opcode=(\d+) status=(\d+) bytes=(\d+) '
               r'sha256=([0-9a-f]{64}) return_bits=(\d+) value3=(\d+) '
               r'null_mask=(\d+) text_hex=([0-9a-f]+|-)\s*$')
    names = ['request', 'opcode', 'status', 'bytes', 'sha256', 'return_bits',
             'value3', 'null_mask', 'text_hex']
    frames = [dict(zip(names, match)) for match in re.findall(pattern, controller, re.MULTILINE)]
    host_pattern = (r'^request=(\d+) opcode=(\d+) admission=(\d+) transport=(\d+) '
                    r'vendor=(\d+) text_bytes=(\d+)\s*$')
    host_names = ['request', 'opcode', 'admission', 'transport', 'vendor', 'text_bytes']
    records = [dict(zip(host_names, match)) for match in re.findall(host_pattern, host, re.MULTILINE)]
    require(len(frames) == 23 and len(records) == 23, 'exact23 controller/host records required')
    for index, (frame, record) in enumerate(zip(frames, records), 1):
        text_size = 0 if frame['text_hex'] == '-' else len(bytes.fromhex(frame['text_hex']))
        require(int(frame['request']) == index and int(record['request']) == index,
                'request order discrepancy')
        require(int(frame['opcode']) == OPERATIONS[index - 1] == int(record['opcode']),
                'opcode discrepancy')
        require(int(frame['status']) == STATUSES.get(index, 0) == int(record['transport']),
                'status discrepancy')
        require(int(record['admission']) == ADMISSIONS[index - 1], 'admission discrepancy')
        require(int(frame['bytes']) == 128 + text_size == 128 + int(record['text_bytes']),
                'reply text extent discrepancy')
        require(frame['return_bits'] == record['vendor'], 'scalar trace discrepancy')
    expected_text = {2: '7.2a', 3: '', 4: 'miles/',
                     9: 'startup bridge23 first', 10: 'startup bridge23 changed'}
    for request, value in expected_text.items():
        frame = frames[request - 1]
        require(frame['null_mask'] == '0' and
                frame['text_hex'] == (value.encode('ascii') + b'\0').hex(),
                'actual owned text discrepancy')
    require(int(frames[5]['return_bits']) != 0, 'vendor startup prerequisite')
    require(frames[10]['return_bits'] == frames[7]['return_bits'], 'previous initial preference')
    require([int(frames[i - 1]['return_bits']) for i in [12, 13, 14, 16]] == [16, 16, 64, 64],
            'signed preference readback discrepancy')
    require(frames[19]['value3'] == '2', 'actual stereo speaker result')
    require('PASS source-facade23 framed requests; no samples/playback' in controller,
            'facade success marker missing')
    require('PASS host ordered shutdown; retained directory bytes=8' in host,
            'host shutdown/retention marker missing')
    require('fixture preference restored before shutdown' in host, 'preference restore missing')
    for request in [5, 15, 18, 19, 22]:
        require('rejected_before_adapter request=' + str(request) + ' retained=8' in host,
                'rejection mutation control missing')
    require('FAIL' not in controller and 'FAIL' not in host, 'recorded failure marker')
    return frames, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.receipt_sha256), 'external receipt pin required')
    receipt_path = BASE / 'evidence-native-v1/receipt.json'
    require(digest(receipt_path) == args.receipt_sha256, 'external receipt pin mismatch')
    receipt = json.loads(receipt_path.read_text())
    helpers = {
        'revision4-tools/receipt.py': BASE.parent / 'live-bridge-candidate/revision4-tools/receipt.py',
        'backend-live25/cleanup.py': BASE / 'cleanup.py',
        'backend-live25/run-facade25.py': Path(__file__).resolve(),
    }
    helper_hashes = {}
    for logical, path in helpers.items():
        native = str(Path('C:/backend-live25') / logical).replace('/', '\\')
        require(receipt['builder_before'].get(native) == digest(path),
                'runtime helper differs from native receipt: ' + logical)
        helper_hashes[logical] = digest(path)
    sys.path.insert(0, str(BASE.parent / 'live-bridge-candidate/revision4-tools'))
    sys.path.insert(0, str(BASE))
    from receipt import verify_pair
    from cleanup import cleanup

    host = BASE / 'private-native-v1/x86-Release/host.exe'
    controller = BASE / 'private-native-v1/amd64-Release/controller.exe'
    pair = verify_pair(receipt_path, args.receipt_sha256, 'Release', host, controller)
    original = Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll')
    require(digest(original) == DLL_SHA256, 'original DLL mismatch')
    plugins = original.parent / 'miles'
    plugin_inputs = plugin_hashes(plugins)
    run = BASE / ('private-run-' + uuid.uuid4().hex[:8])
    run.mkdir(mode=0o700)
    prefix = run / 'prefix'
    name = 'swg_facade25_' + uuid.uuid4().hex[:10]
    result = {'receipt_sha256': args.receipt_sha256, 'runtime_helpers': helper_hashes,
              'pair': pair, 'sink_name': name, 'runs': [], 'process_cleanup': [],
              'private_inputs': {'dll': DLL_SHA256, 'plugins': plugin_inputs}}
    env = os.environ.copy()
    env.update(WINEPREFIX=str(prefix), WINEDEBUG='-all',
               WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d')
    owned_processes = []
    wine_started = False
    target = None

    def owned_wine(arguments, log_name, cwd=None):
        nonlocal wine_started
        with (run / log_name).open('wb') as log:
            process = subprocess.Popen(arguments, env=env, cwd=cwd, stdout=log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            owned_processes.append((log_name, process))
            wine_started = True
            # Output goes directly to a retained file; there is no PIPE deadlock.
            return process.wait(timeout=30)

    def terminate_owned():
        failures = []
        for tag, process in owned_processes:
            record = {'tag': tag, 'pid': process.pid, 'initial_exit': process.poll()}
            try:
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=3)
                record['exit'] = process.returncode
            except Exception as error:
                failures.append(tag + ': ' + str(error))
                record['error'] = str(error)
            result['process_cleanup'].append(record)
        # Independently attempt both stages even if group termination failed.
        if wine_started:
            for option in ['-k', '-w']:
                try:
                    with (run / ('wineserver' + option + '.log')).open('wb') as log:
                        subprocess.run(['wineserver', option], env=env, stdout=log,
                                       stderr=subprocess.STDOUT, timeout=10, check=True)
                except Exception as error:
                    failures.append('wineserver ' + option + ': ' + str(error))
        for tag, process in owned_processes:
            try:
                process.wait(timeout=3)
            except Exception as error:
                failures.append('reap ' + tag + ': ' + str(error))
        result['owned_children_reaped'] = all(process.poll() is not None
                                              for _, process in owned_processes)
        if failures:
            raise RuntimeError('; '.join(failures))

    def unload_owned_sink():
        # Recover ownership by the unique requested name if module creation had
        # an unknown outcome before returning its numeric ID. Never unload all.
        modules = call('pactl', 'list', 'short', 'modules')
        owned = [line.split()[0] for line in modules.splitlines()
                 if len(line.split()) >= 2 and line.split()[1] == 'module-null-sink'
                 and 'sink_name=' + name in line.split()]
        for identifier in owned:
            subprocess.run(['pactl', 'unload-module', identifier], check=True, timeout=15)
        sinks = call('pactl', 'list', 'short', 'sinks')
        result['owned_sink_absent'] = all(len(line.split()) < 2 or line.split()[1] != name
                                           for line in sinks.splitlines())
        require(result['owned_sink_absent'], 'owned null sink remains')

    try:
        result['defaults_before'] = {'sink': call('pactl', 'get-default-sink'),
                                     'source': call('pactl', 'get-default-source')}
        seed = BASE.parent.parent / 'miles-realtime/wine-prefix'
        subprocess.run(['cp', '-a', '--reflink=auto', str(seed), str(prefix)], check=True, timeout=30)
        result['owned_module'] = call('pactl', 'load-module', 'module-null-sink',
                                      'sink_name=' + name, 'rate=22050', 'channels=2', 'format=s16le')
        config = run / 'alsa.conf'
        config.write_text('pcm.!default { type pulse server "unix:/run/user/' + str(os.getuid()) +
                          '/pulse/native" device "' + name + '" }\n')
        env.update(ALSA_CONFIG_PATH=str(config), PULSE_SINK=name, PULSE_SOURCE=name + '.monitor')
        require(owned_wine(['wine', 'reg', 'add', 'HKCU\\Software\\Wine\\Drivers',
                            '/v', 'Audio', '/d', 'alsa', '/f'], 'wine-config.log') == 0,
                'private Wine configuration failed')
        target = prefix / 'drive_c/facade25-private'
        target.mkdir()
        shutil.copy2(original, target / 'Mss32.dll')
        shutil.copytree(plugins, target / 'miles')
        shutil.copy2(host, target / 'host.exe')
        shutil.copy2(controller, target / 'controller.exe')
        runtime_inputs = {name: digest(target / name) for name in ['Mss32.dll', 'host.exe', 'controller.exe']}
        require(runtime_inputs['Mss32.dll'] == DLL_SHA256, 'staged DLL mismatch')
        require(plugin_hashes(target / 'miles') == plugin_inputs, 'staged plugin mismatch')
        for logical, path in helpers.items():
            require(digest(path) == helper_hashes[logical], 'runtime helper changed before launch')
        verify_pair(receipt_path, args.receipt_sha256, 'Release', target / 'host.exe', target / 'controller.exe')
        result['launch_inputs'] = runtime_inputs
        try:
            code = owned_wine(['wine', str(target / 'controller.exe'),
                               'C:\\facade25-private\\host.exe', 'C:\\facade25-private\\Mss32.dll'],
                              'Release.log', target)
        finally:
            if (target / 'host.log').exists():
                shutil.copy2(target / 'host.log', run / 'Release-host-before-cleanup.log')
        result['runs'].append({'config': 'Release', 'returncode': code})
        require(code == 0, 'facade controller nonzero exit')
        text = (run / 'Release.log').read_text(errors='replace')
        host_text = (run / 'Release-host-before-cleanup.log').read_text(errors='replace')
        frames, records = parse_trace(text, host_text)
        require('loaded_dll=c:\\facade25-private\\mss32.dll' in host_text.lower(),
                'loaded module path mismatch')
        result['runs'][0].update(frames=frames, host_records=records, exact_trace=True)
        result['runtime_inputs_after'] = {name: digest(target / name) for name in runtime_inputs}
        result['runtime_inputs_unchanged'] = runtime_inputs == result['runtime_inputs_after']
        result['plugins_unchanged'] = plugin_hashes(target / 'miles') == plugin_inputs
        require(result['runtime_inputs_unchanged'] and result['plugins_unchanged'],
                'runtime input changed')
    except Exception as error:
        result['failure'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        def write(value):
            # Keep the pre-cleanup snapshot and capture any final failure output
            # written before bounded process cleanup completed.
            if target is not None and (target / 'host.log').exists():
                shutil.copy2(target / 'host.log', run / 'Release-host.log')
            value['source_provenance'] = 'native receipt plus named local helper checks; no universal runtime provenance claim'
            (run / 'results.json').write_text(json.dumps(value, indent=2) + '\n')
            print(run)
            print(json.dumps(value))
        cleanup(terminate_owned, unload_owned_sink,
                lambda: {'sink': call('pactl', 'get-default-sink'),
                         'source': call('pactl', 'get-default-source')}, write, result)
    passed = (not result.get('failure') and not result['cleanup_errors'] and
              result.get('defaults_unchanged') and result.get('owned_sink_absent') and
              result.get('owned_children_reaped') and result.get('runtime_inputs_unchanged') and
              result.get('plugins_unchanged') and len(result['runs']) == 1 and
              result['runs'][0].get('exact_trace') and result['runs'][0]['returncode'] == 0)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
