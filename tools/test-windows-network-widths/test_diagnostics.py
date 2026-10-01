"""Negative diagnostics must identify the actual control, not another failure."""
from diagnostics import expected_failure

checks = 0
source = r'C:\fixture\reverted-TcpClient.cpp'
probe = r'C:\fixture\probe.cpp'
header = r'C:\fixture\reverted-headers\Sock.h'
rules = {source: [(550, 'C2664', r".*GetQueuedCompletionStatus.*cannot convert argument 3 from 'unsigned long \*' to 'PULONG_PTR'.*")],
         probe: [(46, 'C2338', 'Sock::handle must be pointer-sized')],
         header: [(19, 'C2371', r"'SOCKET'\s*:\s*redefinition; different basic types")]}
def expect(text, wanted):
    global checks
    assert expected_failure(text, rules) == wanted, text
    checks += 1

def error(path, line, code, message):
    return '%s(%d): error %s: %s\n' % (path, line, code, message)
valid = error(source, 550, 'C2664', "GetQueuedCompletionStatus: cannot convert argument 3 from 'unsigned long *' to 'PULONG_PTR'")
valid_header = error(header, 19, 'C2371', "'SOCKET': redefinition; different basic types")
valid_probe = error(probe, 46, 'C2338', 'Sock::handle must be pointer-sized')
for text in (valid, valid_header, valid_probe, valid_header + valid_probe):
    expect(text, True)
for text in ('', valid.replace(source, r'C:\other.cpp'), valid.replace('(550)', '(551)'),
             valid.replace('GetQueuedCompletionStatus', 'OtherFunction'),
             valid.replace('argument 3', 'argument 2'),
             valid_header.replace("'SOCKET'", "'OTHER'"),
             valid_probe.replace('pointer-sized', 'unrelated'),
             valid_header.replace('(19)', '(20)'),
             valid_probe.replace(probe, source),
             valid + 'LINK : fatal error LNK1104: missing library\n',
             valid + "'cl' is not recognized as an internal or external command\n",
             valid + error(source, 550, 'C1083', 'Cannot open include file'),
             valid + error(source, 550, 'C2664', 'unrelated overload'),
             valid + 'fatal error: unknown tool failure\n'):
    expect(text, False)
print('PASS %d diagnostic classification checks' % checks)
