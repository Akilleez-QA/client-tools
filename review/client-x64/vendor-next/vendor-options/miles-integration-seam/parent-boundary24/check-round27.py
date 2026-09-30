"""Inspect frozen evidence; never compile or execute a candidate."""
from pathlib import Path
import hashlib
import io
import json
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, context):
    if not condition:
        raise RuntimeError(context)


def audit(data, name):
    if name.endswith('.tar'):
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for member in archive.getmembers():
                path = Path(member.name)
                require(member.isfile() and not path.is_absolute() and '..' not in path.parts,
                        'archive path: ' + member.name)
                audit(archive.extractfile(member).read(), member.name)
        return
    path = Path(name)
    allowed = {'.md', '.json', '.log', '.py', '.cpp', '.c', '.cmd', '.sh', '.txt',
               '.h', '.yaml', '.yml', '.patch', '.rsp', '.map', '.stdout', '.stderr', '.sha256'}
    require(path.name.lower() != 'mss.h' and
            (path.suffix in allowed or path.name == '.gitignore'), 'member kind: ' + name)
    require(not data.startswith((b'MZ', b'\x7fELF')) and b'\0' not in data,
            'binary member: ' + name)
    data.decode('utf-8')


for directory, manifest_name, packet_name in [
        ('native-sample27', 'packet-manifest-v2.json', 'packet-v2.tar'),
        ('pipe-live27', 'packet-manifest.json', 'packet-v1.tar')]:
    base = ROOT / directory
    manifest = json.loads((base / manifest_name).read_text())
    with tarfile.open(base / packet_name) as archive:
        members = {m.name: archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}
    for name, record in manifest.items():
        data = members[name]
        sha = record if isinstance(record, str) else record['sha256']
        require(digest(data) == sha, 'packet identity: ' + name)
        if (base / name).is_file():
            require(data == (base / name).read_bytes(), 'local packet identity: ' + name)
        else:
            require(directory == 'pipe-live27' and name.startswith('source/'),
                    'unexpected archive-only member: ' + name)
        if not isinstance(record, str):
            require(len(data) == record['bytes'], 'packet extent: ' + name)
    audit((base / packet_name).read_bytes(), packet_name)

base = ROOT / 'native-sample27'
receipt_bytes = (base / 'evidence-native-v1/receipt.json').read_bytes()
require(digest(receipt_bytes) == '6bd45d43d5d6e4a7430eafa1d360db2c3bd7d0caa40db908eb6452c01f10ca1c',
        'native receipt pin')
receipt = json.loads(receipt_bytes)
require(receipt['passed'] and receipt['stable_sources'] and receipt['before'] == receipt['after'],
        'native stable inputs')
require(receipt['discovery_exit'] == receipt['compile_exit'] == receipt['symbols_exit'] == 0,
        'native tool exits')
require(len(receipt['objects']) == 3 and all(o['machine'] == 0x8664 for o in receipt['objects']),
        'three reported AMD64 objects')
require(receipt['no_link_output'] and not receipt['linked'] and not receipt['executed'],
        'object-only scope')
expected = {'__imp_AIL_' + n for n in ['allocate_sample_handle', 'set_named_sample_file',
                                     'sample_ms_position', 'end_sample', 'release_sample_handle']}
require(set(receipt['undefined_miles_imports']) == expected, 'five actual imports')
for path, sha in receipt['sources_before'].items():
    relative = path.replace('\\', '/').split('C:/native-sample27/')[1]
    require(digest((ROOT / relative).read_bytes()) == sha, 'native source: ' + relative)
require(any(Path(n.replace('\\', '/')).name == 'Mss.h' and
            sha == '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e'
            for n, sha in receipt['before']['headers'].items()), 'actual SDK header')
(base / 'parent-build-attribution.json').write_text(json.dumps({
    'scope': 'Parent source/receipt attribution; compiler not rerun and private COFF objects not read',
    'passed': True, 'receipt_sha256': digest(receipt_bytes), 'objects_reported': 3,
    'undefined_real_imports': sorted(expected)}, indent=2) + '\n')

base = ROOT / 'pipe-live27'
evidence = base / 'evidence-runtime-v1'
receipt_bytes = (evidence / 'results.json').read_bytes()
require(digest(receipt_bytes) == 'a4ed5315e25ba8c7f4701f774d5625f8e0d5a0fe7e93144a53a75afd2124791c',
        'runtime receipt pin')
receipt = json.loads(receipt_bytes)
client = (evidence / 'Release.log').read_text()
host = (evidence / 'Release-host.log').read_text()
clients = [dict(re.findall(r'(\w+)=([^ ]+)', line)) for line in client.splitlines()
           if line.startswith('reply request=')]
hosts = [dict(re.findall(r'(\w+)=([^ ]+)', line)) for line in host.splitlines()
         if line.startswith('request=')]
require(len(clients) == len(hosts) == 22, 'paired raw record count')
operations = [4096, 4101, 34, 56, 14, 53, 30, 31, 29, 27, 35, 19, 35, 19, 26, 30, 19, 26, 19, 52, 26, 4109]
admissions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 18, 19]
for i, (c, s) in enumerate(zip(clients, hosts), 1):
    require(int(c['request']) == int(s['request']) == i and
            int(c['opcode']) == int(s['opcode']) == operations[i - 1], 'order/opcode')
    require(int(c['status']) == int(s['transport']) == {16: 3, 17: 2, 18: 2, 21: 4097}.get(i, 0),
            'status')
    require(int(s['admission']) == admissions[i - 1], 'admission')
require([int(clients[i - 1]['return_bits']) for i in [12, 14, 19]] == [2, 0, 0], 'room changes')
states = re.findall(r'^state request=(\d+) field=([^ ]+) actual=(\w+) expected=(\w+)$', host, re.M)
require(len(states) == 16 and all(a == e for _, _, a, e in states), 'fixed state bit records')
require(receipt['defaults_before'] == receipt['defaults_after'] and receipt['defaults_unchanged'],
        'host defaults')
require(receipt['owned_children_reaped'] and receipt['owned_sink_absent'] and
        not receipt['cleanup_errors'] and not receipt.get('failure'), 'cleanup')
require(receipt['launch_inputs'] == receipt['runtime_inputs_after'] and receipt['plugins_unchanged'],
        'runtime input stability')
require(receipt['runs'][0]['returncode'] == 0 and 'PASS host27 ordered shutdown' in host, 'normal exit')
(base / 'parent-runtime-attribution.json').write_text(json.dumps({
    'scope': 'Parent trace inspection of one worker run; not a second vendor execution',
    'passed': True, 'runtime_sha256': digest(receipt_bytes), 'paired_records': 22,
    'state_bit_records': 16, 'room_readbacks': [2, 0, 0], 'cleanup_and_input_checks': True,
    'limits': ['idle serve only', 'no sample playback/file callbacks',
               'no engine/Bink', 'no native Miles64 runtime']}, indent=2) + '\n')
print('PASS round27 packet/source/receipt/trace attribution')
