"""One receipted Release live slice; private Wine prefix/null sink; explicit gates."""
from pathlib import Path
import sys, os, json, hashlib, subprocess, uuid, shutil, re
base = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def call(*argv):
    return subprocess.check_output(argv, text=True, timeout=15).strip()
require(len(sys.argv) == 2, 'external build receipt pin required')
receipt_path = base / 'evidence-native-v2/receipt.json'
require(digest(receipt_path) == sys.argv[1], 'receipt pin mismatch')
receipt = json.loads(receipt_path.read_text())
helpers = {'revision4-tools/receipt.py': base.parent / 'live-bridge-candidate/revision4-tools/receipt.py', 'startup-bridge23/cleanup.py': base / 'cleanup.py', 'startup-bridge23/run-private.py': Path(__file__).resolve()}
helper_hashes = {}
for logical, p in helpers.items():
    native = str(Path('C:/startup-bridge23/v2') / logical).replace('/', '\\')
    require(receipt['builder_before'].get(native) == digest(p), 'runtime helper differs from build receipt: ' + logical)
    helper_hashes[logical] = digest(p)
sys.path.insert(0, str(base.parent / 'live-bridge-candidate/revision4-tools'))
sys.path.insert(0, str(base))
from receipt import verify_pair
from cleanup import cleanup
host = base / 'private-native-v2/x86-Release/host.exe'
controller = base / 'private-native-v2/amd64-Release/controller.exe'
pair = verify_pair(receipt_path, sys.argv[1], 'Release', host, controller)
original = Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll')
dllhash = '0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
require(digest(original) == dllhash, 'original DLL identity')
plugins = original.parent / 'miles'
plugin_hashes = {str(p.relative_to(plugins)): digest(p) for p in sorted(plugins.rglob('*')) if p.is_file()}
run = base / ('private-run-' + uuid.uuid4().hex[:8])
run.mkdir(mode=448)
prefix = run / 'prefix'
old = base.parent.parent / 'miles-realtime/wine-prefix'
subprocess.run(['cp', '-a', '--reflink=auto', str(old), str(prefix)], check=True)
before = {'sink': call('pactl', 'get-default-sink'), 'source': call('pactl', 'get-default-source')}
name = 'swg_startup23_' + uuid.uuid4().hex[:10]
module = None
result = dict(receipt_sha256=sys.argv[1], runtime_helpers=helper_hashes, defaults_before=before, sink_name=name, runs=[], private_inputs={'dll': dllhash, 'plugins': plugin_hashes}, pair=pair)
env = os.environ.copy()
env.update(WINEPREFIX=str(prefix), WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d', WINEDEBUG='-all')
try:
    module = call('pactl', 'load-module', 'module-null-sink', 'sink_name=' + name, 'rate=22050', 'channels=2', 'format=s16le')
    result['owned_module'] = module
    config = run / 'alsa.conf'
    config.write_text('pcm.!default { type pulse server "unix:/run/user/' + str(os.getuid()) + '/pulse/native" device "' + name + '" }\n')
    env.update(ALSA_CONFIG_PATH=str(config), PULSE_SINK=name, PULSE_SOURCE=name + '.monitor')
    with (run / 'wine-config.log').open('wb') as log:
        subprocess.run(['wine', 'reg', 'add', 'HKCU\\Software\\Wine\\Drivers', '/v', 'Audio', '/d', 'alsa', '/f'], env=env, stdout=log, stderr=subprocess.STDOUT, timeout=30, check=True)
    target = prefix / 'drive_c/startup23-private'
    target.mkdir()
    shutil.copy2(original, target / 'Mss32.dll')
    shutil.copytree(plugins, target / 'miles')
    shutil.copy2(host, target / 'host.exe')
    shutil.copy2(controller, target / 'controller.exe')
    runtime_inputs = {p: digest(target / p) for p in ['Mss32.dll', 'host.exe', 'controller.exe']}
    require(runtime_inputs['Mss32.dll'] == dllhash, 'staged DLL mismatch')
    require({str(p.relative_to(target / 'miles')): digest(p) for p in (target / 'miles').rglob('*') if p.is_file()} == plugin_hashes, 'staged plugins mismatch')
    for logical, p in helpers.items():
        require(digest(p) == helper_hashes[logical], 'runtime helper changed before launch')
    verify_pair(receipt_path, sys.argv[1], 'Release', target / 'host.exe', target / 'controller.exe')
    result['launch_inputs'] = runtime_inputs
    with (run / 'Release.log').open('wb') as log:
        try:
            process = subprocess.run(['wine', str(target / 'controller.exe'), 'C:\\startup23-private\\host.exe', 'C:\\startup23-private\\Mss32.dll'], env=env, cwd=target, stdout=log, stderr=subprocess.STDOUT, timeout=30)
            code = process.returncode
        except subprocess.TimeoutExpired:
            code = 'timeout'
    if (target / 'host.log').exists():
        shutil.copy2(target / 'host.log', run / 'Release-host.log')
    text = (run / 'Release.log').read_text(errors='replace')
    hosttext = (run / 'Release-host.log').read_text(errors='replace') if (run / 'Release-host.log').exists() else ''
    pattern = 'reply request=(\\d+) opcode=(\\d+) status=(\\d+) bytes=(\\d+) sha256=([0-9a-f]{64}) return_bits=(\\d+) value3=(\\d+) null_mask=(\\d+) text_hex=([0-9a-f]+|-)'
    frames = [dict(zip(['request', 'opcode', 'status', 'bytes', 'sha256', 'return_bits', 'value3', 'null_mask', 'text_hex'], m)) for m in re.findall(pattern, text)]
    expected_ops = [4096, 4101, 34, 34, 34, 56, 10, 10, 12, 12, 33, 10, 33, 10, 33, 10, 14, 53, 53, 53, 52, 10, 4109]
    expected_status = {5: 3, 15: 3, 18: 3, 19: 2, 22: 4097}
    frame_check = len(frames) == 23 and all((int(f['request']) == i and int(f['opcode']) == expected_ops[i - 1] and (int(f['status']) == expected_status.get(i, 0)) and (int(f['bytes']) >= 128) for i, f in enumerate(frames, 1)))
    rec = dict(config='Release', returncode=code, frames=frames, exact_order_status=frame_check, exact_count='PASS 23 framed requests' in text, cleanup='PASS host ordered shutdown; retained directory bytes=8' in hosttext, loaded_exact='loaded_dll=C:\\startup23-private\\Mss32.dll'.lower() in hosttext.lower(), no_failure='FAIL' not in text and 'FAIL' not in hosttext, rejected_controls=all(('rejected_before_adapter request=' + str(i) + ' ' in hosttext for i in [5, 15, 18, 19, 22])))
    result['runs'].append(rec)
    result['runtime_inputs_after'] = {p: digest(target / p) for p in runtime_inputs}
    result['runtime_inputs_unchanged'] = runtime_inputs == result['runtime_inputs_after']
    result['plugins_unchanged'] = {str(p.relative_to(target / 'miles')): digest(p) for p in (target / 'miles').rglob('*') if p.is_file()} == plugin_hashes
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:

    def write(value):
        value['source_provenance'] = 'frozen native receipt and explicitly verified local runtime helpers'
        (run / 'results.json').write_text(json.dumps(value, indent=2) + '\n')
        print(run)
        print(json.dumps(value))
    cleanup(lambda: subprocess.run(['wineserver', '-k'], env=env, timeout=10, check=True), lambda: subprocess.run(['pactl', 'unload-module', module], check=True, timeout=15) if module else None, lambda: {'sink': call('pactl', 'get-default-sink'), 'source': call('pactl', 'get-default-source')}, write, result)
passed = not result.get('failure') and (not result['cleanup_errors']) and result.get('defaults_unchanged') and result.get('runtime_inputs_unchanged') and result.get('plugins_unchanged') and (len(result['runs']) == 1) and all((x['returncode'] == 0 and all((x[k] for k in ['exact_order_status', 'exact_count', 'cleanup', 'loaded_exact', 'no_failure', 'rejected_controls'])) for x in result['runs']))
raise SystemExit(not passed)
