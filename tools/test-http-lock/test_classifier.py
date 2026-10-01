"""Portable rejection-classifier controls; optionally replay original native logs."""
import argparse
from pathlib import Path
from run import stock_x64_rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recorded-results', type=Path)
    args = parser.parse_args()
    rows = Path(__file__).with_name('stock-x64-diagnostics.txt').read_text().splitlines()
    header = r'C:\fixture\VeCritsec.hpp'
    lines = ['C:\\fixture\\' + row for row in rows]
    log = '\n'.join(lines)
    checks = 0

    def check(expected, code, text, path=header):
        nonlocal checks
        if stock_x64_rejected(code, text, path) != expected:
            raise AssertionError('classifier control {}'.format(checks + 1))
        checks += 1

    check(True, 2, log)
    for code in (0, 1, 'timeout', None, -1, True):
        check(False, code, log)
    for index in range(len(lines)):
        check(False, 2, '\n'.join(lines[:index] + lines[index + 1:]))
        check(False, 2, log + '\n' + lines[index])
    for changed in (
            log.replace('(43)', '(44)', 1),
            log.replace('C4235', 'C9999', 1),
            log.replace(' : error C4235:', ' error C4235:', 1),
            log.replace('keyword not supported', 'unexpected keyword', 1),
            log.replace('C:\\fixture\\', 'C:\\unrelated\\', 1),
            log + '\nLINK : fatal error LNK1120: 1 unresolved externals',
            log + '\nprobe.cpp(1) : error C9999: unrelated failure',
            log + '\nerror: command failed',
            '\n'.join(reversed(lines)),
            log + '\nThe system cannot find the path specified.',
            'C4235'):
        check(False, 2, changed)
    check(False, 2, log, r'C:\different\VeCritsec.hpp')
    if args.recorded_results:
        for config in ('Debug', 'Release'):
            case = config + '-x64-stock'
            recorded = (args.recorded_results / case / 'build.log').read_text()
            path = 'C:\\http-candidate23\\results-v2\\' + case + '\\VeCritsec.hpp'
            check(True, 2, recorded, path)
            check(False, 2, recorded + '\nLINK : fatal error LNK1120: unrelated', path)
    print('PASS {} classifier controls (no native execution)'.format(checks))


if __name__ == '__main__':
    main()
