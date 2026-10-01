"""Ensure unrelated build failures cannot satisfy the assembly control."""
from pathlib import Path
from run import assembly_failure

source = Path('baseline.cpp').resolve()
def error(code, line=16, path=source):
    return ('%s(%d): error %s: diagnostic\n' % (path, line, code)).encode()

valid = error('C2485') + error('C4235', 18)
assert assembly_failure(valid, source)
assert assembly_failure(valid + error('C2065', 20) + error('C1903', 30), source)
for invalid in (b'', error('C2485'), error('C4235', 18),
                valid + error('C1083'), valid + error('C2065', 99),
                valid + error('C2065', 20, Path('other.cpp').resolve()),
                valid + b'LINK : fatal error LNK1104: cannot open file\n',
                valid + b"'cl' is not recognized as an internal or external command\n",
                valid + b'error: compiler unavailable\n'):
    assert not assembly_failure(invalid, source), invalid
print('PASS 12 diagnostic classification checks')
