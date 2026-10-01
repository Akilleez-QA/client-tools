"""Ensure unrelated build failures cannot satisfy the assembly control."""
from pathlib import Path
from run import assembly_failure

checks = 0
def expect(output, source, expected):
    global checks
    assert assembly_failure(output, source) == expected, output
    checks += 1

source = Path('baseline.cpp').resolve()
def error(code, line=16, path=source):
    return ('%s(%d): error %s: diagnostic\n' % (path, line, code)).encode()

valid = error('C2485') + error('C4235', 18)
expect(valid, source, True)
expect(valid + error('C2065', 20) + error('C1903', 30), source, True)
for invalid in (b'', error('C2485'), error('C4235', 18),
                valid + error('C1083'), valid + error('C2065', 99),
                valid + error('C2065', 20, Path('other.cpp').resolve()),
                valid + b'LINK : fatal error LNK1104: cannot open file\n',
                valid + b"'cl' is not recognized as an internal or external command\n",
                valid + b'error: compiler unavailable\n'):
    expect(invalid, source, False)
modern_pairs = (('C3260', 20), ('C7553', 28), ('C2485', 36),
                ('C2144', 36), ('C2601', 36), ('C2485', 47),
                ('C2601', 47), ('C1004', 59))
modern = valid + b''.join(error(code, line) for code, line in modern_pairs)
expect(modern, source, True)
for code, line in modern_pairs:
    expect(modern + error(code, 99), source, False)
    expect(modern + error(code, line, Path('other.cpp').resolve()), source, False)
expect(modern + error('C1083', 20), source, False)
expect(modern + b'LINK : fatal error LNK1104: missing library\n', source, False)
print('PASS %d diagnostic classification checks' % checks)
