"""Compare Win32 PEs, rejecting unsafe metadata spans before normalization."""
import argparse
import hashlib
from pathlib import Path
import struct
import json


def normalize(data):
    b = bytearray(data)

    def span(offset, size):
        if offset < 0 or size < 0 or offset + size > len(b):
            raise ValueError('PE span outside file')
        return offset

    def u16(offset):
        return struct.unpack_from('<H', b, span(offset, 2))[0]

    def u32(offset):
        return struct.unpack_from('<I', b, span(offset, 4))[0]

    def overlaps(a, n, c, m):
        return n > 0 and m > 0 and a < c + m and c < a + n

    if b[:2] != b'MZ':
        raise ValueError('missing DOS signature')
    pe = u32(60)
    span(pe, 24)
    if pe < 64 or b[pe:pe + 4] != b'PE\0\0' or u16(pe + 4) != 0x14c:
        raise ValueError('expected i386 PE image')
    op = pe + 24
    optional_size = u16(pe + 20)
    span(op, optional_size)
    if optional_size < 96 or u16(op) != 0x10b:
        raise ValueError('expected Win32 optional header')
    directory_count = u32(op + 92)
    if directory_count > (optional_size - 96) // 8:
        raise ValueError('data directories exceed optional header')
    num = u16(pe + 6)
    if not 1 <= num <= 96:
        raise ValueError('invalid PE section count')
    sh = op + optional_size
    span(sh, 40 * num)
    header_size = u32(op + 60)
    if not sh + 40 * num <= header_size <= len(b):
        raise ValueError('invalid SizeOfHeaders')
    sections = []
    hashes = {}
    for i in range(num):
        o = sh + 40 * i
        name = bytes(b[o:o + 8]).rstrip(b'\0').decode('ascii')
        if not name or name in hashes:
            raise ValueError('empty or duplicate section name')
        vs, va, rs, rp = struct.unpack_from('<IIII', b, o + 8)
        flags = u32(o + 36)
        size = max(vs, rs)
        if va + size > 0x100000000 or (size and va < header_size):
            raise ValueError('invalid section virtual range')
        if rs:
            span(rp, rs)
            if rp < header_size:
                raise ValueError('section overlaps PE headers')
        for old_va, old_size, old_rp, old_rs, _ in sections:
            if overlaps(va, size, old_va, old_size) or overlaps(rp, rs, old_rp, old_rs):
                raise ValueError('overlapping PE sections')
        sections.append((va, size, rp, rs, flags))
        hashes[name] = hashlib.sha256(b[rp:rp + rs]).hexdigest()

    def position(rva, size):
        for va, _, rp, rs, _ in sections:
            if va <= rva and rva - va + size <= rs:
                return span(rp + rva - va, size)
        raise ValueError('RVA span is not backed by section file data')

    def directory(index):
        if index >= directory_count:
            return 0, 0
        rva, size = struct.unpack_from('<II', b, op + 96 + index * 8)
        if bool(rva) != bool(size):
            raise ValueError('incomplete data directory')
        return rva, size

    fields = []

    def field(offset, size, name):
        span(offset, size)
        for _, _, rp, rs, flags in sections:
            if flags & (0x20000000 | 0x20) and overlaps(offset, size, rp, rs):
                raise ValueError('normalization would modify executable/code section')
        if any(overlaps(offset, size, old, length) for old, length, _ in fields):
            raise ValueError('overlapping normalization fields')
        fields.append((offset, size, name))

    field(pe + 8, 4, 'COFF timestamp')
    rva, size = directory(0)
    if rva:
        if size < 40:
            raise ValueError('truncated export directory')
        field(position(rva, size) + 4, 4, 'export timestamp')
    rva, size = directory(6)
    if rva:
        if size % 28:
            raise ValueError('partial debug directory entry')
        start = position(rva, size)
        for offset in range(start, start + size, 28):
            field(offset + 4, 4, 'debug timestamp')
            typ, length, address, pointer = struct.unpack_from('<IIII', b, offset + 12)
            if length:
                span(pointer, length)
                if pointer < header_size:
                    raise ValueError('debug data overlaps PE headers')
                if address and position(address, length) != pointer:
                    raise ValueError('debug data RVA and file pointer disagree')
            elif address or pointer:
                raise ValueError('empty debug data has a location')
            if typ == 2:
                if length < 25 or b[pointer:pointer + 4] != b'RSDS' or 0 not in b[pointer + 24:pointer + length]:
                    raise ValueError('truncated RSDS record or missing PDB path terminator')
                field(pointer + 20, 4, 'PDB age')
    for offset, size, _ in fields:
        b[offset:offset + size] = b'\0' * size
    return b, fields, hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    before, after = args.before.read_bytes(), args.after.read_bytes()
    result = {
        'normalized_equal': False,
        'before_sha256': hashlib.sha256(before).hexdigest(),
        'after_sha256': hashlib.sha256(after).hexdigest(),
        'before_bytes': len(before), 'after_bytes': len(after),
        'diagnostic_markers_absent': all(x not in before and x not in after for x in
            [b'fpu-transition.log', b'fpu-runtime.log', b'collision-entry', b'dpvs-entry']),
    }
    try:
        a, af, ah = normalize(before)
        b, bf, bh = normalize(after)
        if af != bf:
            raise ValueError('normalization locations differ between images')
        result.update(normalized_equal=a == b, before_normalized_fields=af,
                      after_normalized_fields=bf,
                      sections_equal={s: ah.get(s) == bh.get(s) for s in ah.keys() | bh.keys()})
    except (ValueError, struct.error) as exc:
        result['validation_error'] = str(exc)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['normalized_equal'] and result['diagnostic_markers_absent'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
