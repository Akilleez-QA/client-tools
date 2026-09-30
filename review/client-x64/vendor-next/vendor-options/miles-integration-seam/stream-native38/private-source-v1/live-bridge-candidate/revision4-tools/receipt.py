"""Pinned build receipt verification. No runtime execution or current-source inference."""
from pathlib import Path
import hashlib
import json
import struct

class ReceiptError(ValueError):
    pass

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def machine(path):
    with Path(path).open('rb') as stream:
        if stream.read(2) != b'MZ':
            raise ReceiptError('missing DOS signature')
        stream.seek(60)
        offset = struct.unpack('<I', stream.read(4))[0]
        stream.seek(offset)
        if stream.read(4) != b'PE\0\0':
            raise ReceiptError('missing PE signature')
        return struct.unpack('<H', stream.read(2))[0]

def verify_pair(receipt_path, expected_digest, config, host, controller):
    raw = Path(receipt_path).read_bytes()
    if len(expected_digest) != 64 or hashlib.sha256(raw).hexdigest() != expected_digest.lower():
        raise ReceiptError('receipt digest differs from external pin')
    receipt = json.loads(raw)
    if receipt.get('schema') != 'miles-build-receipt-v4' or config not in ('Debug', 'Release'):
        raise ReceiptError('receipt schema or configuration')
    if not receipt.get('stable_matrix') or receipt['builder_before'] != receipt['builder_after'] or receipt['source_snapshot_before'] != receipt['source_snapshot_after']:
        raise ReceiptError('unstable build matrix receipt')
    verified = []
    for architecture, path, expected_machine in [('x86', host, 0x14c), ('amd64', controller, 0x8664)]:
        records = [x for x in receipt['builds'] if x['config'] == config and x['architecture'] == architecture]
        if len(records) != 1:
            raise ReceiptError('missing or duplicate build identity')
        record = records[0]
        if record['exit_code'] != 0 or not record['inputs_unchanged'] or record['before'] != record['after']:
            raise ReceiptError('unsuccessful or unstable build')
        if not record['before']['sources'] or not record['before']['headers'] or not record['before']['tools']:
            raise ReceiptError('incomplete input provenance')
        output = record['output']
        if not Path(path).is_file():
            raise ReceiptError('selected output missing')
        if output['machine'] != expected_machine or machine(path) != expected_machine:
            raise ReceiptError('selected output architecture mismatch')
        if digest(path) != output['sha256']:
            raise ReceiptError('selected output bytes differ from build-time hash')
        verified.append({'architecture': architecture, 'path': str(Path(path).resolve()),
                         'sha256': output['sha256'], 'machine': expected_machine})
    return {'receipt_sha256': expected_digest.lower(), 'configuration': config, 'outputs': verified,
            'input_provenance': 'frozen build receipt; no post-run source hashing'}
