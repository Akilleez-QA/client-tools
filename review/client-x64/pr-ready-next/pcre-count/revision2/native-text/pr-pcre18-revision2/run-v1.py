#!/usr/bin/env python3
"""Structural caller binding plus a safe real-provider API-contract probe."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

CALLER = Path('src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp')
CALL = 'pcre_exec(regularExpression,NULL,pathAsString.c_str(),pathAsString.length(),0,0,&captureData[0],subscriptCount)'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def assert_caller(source):
    # Deliberately lexical, not a C++ parser or execution of the production caller.
    source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
    compact = re.sub(r'\s+', '', source)
    required = ['intconstmaxSupportedCaptureCount=10;',
                'intconstsubscriptCount=(maxSupportedCaptureCount+1)*3;',
                'intcaptureData[subscriptCount];', CALL + ';if(resultCode<0)']
    if any(compact.count(fragment) != 1 for fragment in required):
        raise ValueError('production caller declaration/argument/result guard does not match the reviewed structure')
    if compact.count('pcre_exec(') != 1:
        raise ValueError('expected exactly one production pcre_exec call')
    return 33

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--include-dir', type=Path)
    parser.add_argument('--library', type=Path)
    parser.add_argument('--bits', type=int, choices=[32, 64])
    parser.add_argument('--configuration', choices=['Debug', 'Release'])
    args = parser.parse_args()
    out = args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    report = {'passed': False, 'provider_executed': False,
              'scope': 'lexical production binding and separately compiled safe API-contract probe'}
    try:
        caller = (args.checkout / CALLER).resolve()
        source = caller.read_text(encoding='utf-8')
        slots = assert_caller(source)
        report['caller'] = {'path': str(caller), 'sha256': digest(caller)}
        # Safe mutation: validate text only, never compile or execute the old call.
        reverted, replacements = re.subn(r'(&captureData\[0\],\s*)subscriptCount', r'\1sizeof(captureData)', source)
        if replacements != 1:
            raise ValueError('cannot construct unique safe reversion control')
        try:
            assert_caller(reverted)
        except ValueError:
            report['safe_reversion_rejected_before_provider'] = True
        else:
            raise ValueError('structural assertion accepted the unsafe byte-count expression')
        report['capacity_elements'] = slots
        if not args.check_only:
            if any(value is None for value in [args.include_dir, args.library, args.bits, args.configuration]):
                raise ValueError('provider runs require --include-dir --library --bits --configuration')
            header = (args.include_dir / 'pcre.h').resolve()
            library = args.library.resolve()
            probe = Path(__file__).with_name('probe.c').resolve()
            compiler = shutil.which('cl')
            if not compiler:
                raise ValueError('cl not found; use the matching VS2013 developer command prompt')
            report['inputs'] = {str(p): digest(p) for p in [header, library, probe, Path(__file__).resolve(), Path(compiler)]}
            (out / 'capacity.h').write_text('#define CAPTURE_SLOTS %d\n#define EXPECT_BITS %d\n' % (slots, args.bits))
            exe = out / 'probe.exe'
            command = [compiler, '/nologo', '/TC', '/W4', '/WX', '/showIncludes', '/DPCRE_STATIC',
                       '/MTd' if args.configuration == 'Debug' else '/MT',
                       '/I' + str(args.include_dir.resolve()), '/I' + str(out),
                       str(probe), str(library), '/Fo' + str(out / 'probe.obj'), '/Fe' + str(exe)]
            report['command'] = command
            env = dict(os.environ, VSLANG='1033')
            built = subprocess.run(command, cwd=out, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
            (out / 'build.log').write_bytes(built.stdout)
            report['build_exit'] = built.returncode
            includes = re.findall(r'Note: including file:\s*(.+)', built.stdout.decode('utf-8', 'replace'))
            report['included_headers'] = {str(Path(p.strip())): digest(Path(p.strip())) for p in includes}
            if built.returncode:
                raise ValueError('native compile/link failed; see build.log')
            report['executable_sha256'] = digest(exe)
            report['provider_executed'] = True
            run = subprocess.run([str(exe)], cwd=out, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
            (out / 'run.log').write_bytes(run.stdout)
            report['run_exit'] = run.returncode
            if run.returncode or run.stdout.decode('ascii', 'replace').splitlines().count('PASS 25 bounded correct-count checks') != 1:
                raise ValueError('provider probe failed or did not report exactly 25 checks')
            report['checks'] = 25
        report['passed'] = True
    except Exception as error:
        report['error'] = str(error)
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    sys.exit(main())
