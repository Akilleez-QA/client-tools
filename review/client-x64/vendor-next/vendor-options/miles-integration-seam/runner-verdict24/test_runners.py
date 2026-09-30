"""Pure runner tests: no compiler, native executable, VM, Wine, or vendor launch."""
from pathlib import Path
from unittest.mock import patch
from copy import deepcopy
import contextlib
import hashlib
import inspect
import io
import json
import platform
import runpy
import subprocess
import sys
import tempfile

from verdict import acceptance_errors

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / 'pipe-drain23'
# Separate test declarations make accidental runner policy changes observable.
SPECS = {
    'run-native.py': (
        ['idle', 'exchange', 'late-read', 'late-peer-error', 'buffered-input',
         'partial-input', 'queued-write', 'partial-write', 'backpressure',
         'completed-write', 'first-fault', 'external-abort', 'timeout'],
        {'late-read', 'late-peer-error', 'buffered-input', 'partial-input',
         'partial-write', 'backpressure', 'completed-write'}),
    'run-supplement.py': (
        ['exchange-session', 'ordered-close-input', 'session-timeout'],
        {'ordered-close-input', 'session-timeout'}),
}
SCENARIOS = [
    'success', 'old-build-failure', 'candidate-build-failure',
    'wrong-old-exit', 'wrong-candidate-exit', 'case-timeout', 'build-timeout',
    'missing-case', 'duplicate-case', 'missing-build', 'duplicate-build',
    'matches-contradiction', 'spoofed-expectation', 'unknown-case',
]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


class ChildDouble:
    def __init__(self, cases, old_failure, scenario):
        self.cases, self.old_failure, self.scenario = cases, old_failure, scenario
        self.calls = []
        self.injected = False

    def run(self, argv, *, cwd, capture_output, timeout):
        # Called directly by subprocess.run replacement, so caller is the real runner.
        state = inspect.currentframe().f_back.f_globals
        check(state['cases'] == self.cases and state['old_failure'] == self.old_failure,
              'runner changed declared policy')
        variant = cwd.name.split('-')[0]
        check(variant in ('old', 'candidate') and capture_output, 'unknown launch')
        build = argv[0] == 'cmd'
        name = 'build' if build else argv[1]
        check(build or name in self.cases, 'attempted undeclared executable case')
        self.calls.append([variant, name])
        if build:
            check(argv[:3] == ['cmd', '/d', '/c'] and timeout == 60, 'build invocation')
            if self.scenario == variant + '-build-failure':
                return subprocess.CompletedProcess(argv, 2, b'synthetic compiler failure\n', b'')
            if self.scenario == 'build-timeout' and variant == 'old':
                raise subprocess.TimeoutExpired(argv, timeout, output=b'synthetic build timeout\n')
            return subprocess.CompletedProcess(argv, 0, b'synthetic build success\n', b'')
        check(argv[0].endswith('fixture.exe') and timeout == 15, 'case invocation')
        if self.scenario == 'case-timeout' and variant == 'old' and name == self.cases[0]:
            raise subprocess.TimeoutExpired(argv, timeout, output=b'synthetic case timeout\n')
        if variant == 'candidate' and name == self.cases[-1] and not self.injected:
            self.injected = True
            records = state['results']
            first_case = next(i for i, row in enumerate(records) if 'case' in row)
            if self.scenario == 'missing-case':
                del records[first_case]
            elif self.scenario == 'duplicate-case':
                records.append(dict(records[first_case]))
            elif self.scenario == 'missing-build':
                del records[0]
            elif self.scenario == 'duplicate-build':
                records.append(dict(records[0]))
            elif self.scenario == 'matches-contradiction':
                records[first_case]['matches'] = False
            elif self.scenario == 'spoofed-expectation':
                records[first_case].update(exit=7, expected=7, matches=True)
            elif self.scenario == 'unknown-case':
                records.append(dict(variant='candidate', case='undeclared', exit=0, matches=True))
        code = int(variant == 'old' and name in self.old_failure)
        if self.scenario == 'wrong-old-exit' and variant == 'old' and name in self.old_failure:
            code = 0
        if self.scenario == 'wrong-candidate-exit' and variant == 'candidate' and name == self.cases[0]:
            code = 9
        return subprocess.CompletedProcess(argv, code, b'synthetic child output\n', b'')


def exercise(script, scenario, original=False):
    cases, old_failure = SPECS[script]
    double = ChildDouble(cases, old_failure, scenario)
    output = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='runner-test-', dir=ROOT) as tmp:
        destination = Path(tmp)
        (destination / 'sentinel.cpp').write_text('// pure local test input\n')
        def root_double(value):
            wanted = 'C:/pipe-drain23' if original else 'C:/runner-verdict24'
            check(value == wanted, 'runner tried an unexpected root')
            return destination
        code = 0
        target = (FROZEN if original else ROOT) / script
        # Popen is a tripwire: even an accidental bypass of the run double must fail.
        with patch('pathlib.Path', new=root_double), \
             patch('subprocess.run', new=double.run), \
             patch('subprocess.Popen', side_effect=AssertionError('real process forbidden')), \
             contextlib.redirect_stdout(output):
            try:
                runpy.run_path(str(target), run_name='__main__')
            except SystemExit as error:
                code = error.code
        prefix = 'supplement-' if script == 'run-supplement.py' else ''
        result_file = destination / (prefix + 'results.json')
        check(result_file.exists(), 'runner did not persist result evidence')
        records = json.loads(result_file.read_text())
        verdict = None
        if not original:
            verdict_file = destination / (prefix + 'verdict.json')
            check(verdict_file.exists(), 'runner did not persist final verdict')
            verdict = json.loads(verdict_file.read_text())
        expected = 0 if original or scenario == 'success' else 1
        check(type(code) is int and code == expected,
              '{} {}: exit {!r}, wanted {}'.format(script, scenario, code, expected))
        if not original:
            check(verdict['passed'] == (expected == 0), 'verdict/process contradiction')
            check(bool(verdict['errors']) == (expected == 1), 'diagnostics/process contradiction')
        return dict(script=script, original=original, scenario=scenario, exit=code,
                    expected=expected, calls=double.calls, records=records,
                    verdict=verdict, output=output.getvalue())


def complete_records():
    records = []
    for variant in ('old', 'candidate'):
        records.append(dict(variant=variant, stage='build', exit=0))
        for case in ['positive', 'negative']:
            code = int(variant == 'old' and case == 'negative')
            records.append(dict(variant=variant, case=case, exit=code, expected=code, matches=True))
    return records


def helper_controls():
    cases, old_failure = ['positive', 'negative'], {'negative'}
    base = complete_records()
    checks = [('complete-success', base, False), ('empty-results', [], True),
              ('nonlist-results', {}, True)]
    for name, mutate in [
        ('missing-case', lambda r: r.pop(1)),
        ('duplicate-case', lambda r: r.append(dict(r[1]))),
        ('missing-build', lambda r: r.pop(0)),
        ('duplicate-build', lambda r: r.append(dict(r[0]))),
        ('wrong-exit-matches-true', lambda r: r[1].update(exit=9, matches=True)),
        ('build-failure', lambda r: r[0].update(exit=1)),
        ('timeout-with-zero-exit', lambda r: r[1].update(timeout=True)),
        ('reported-matches-false', lambda r: r[1].update(matches=False)),
        ('reported-matches-not-bool', lambda r: r[1].update(matches=1)),
        ('spoofed-expected', lambda r: r[1].update(exit=9, expected=9, matches=True)),
        ('missing-exit', lambda r: r[1].pop('exit')),
        ('bool-exit', lambda r: r[1].update(exit=False)),
        ('unknown-variant', lambda r: r[1].update(variant='other')),
        ('unknown-case', lambda r: r[1].update(case='other')),
        ('ambiguous-build-case', lambda r: r[0].update(case='positive')),
        ('nonobject-record', lambda r: r.append(None)),
    ]:
        rows = deepcopy(base)
        mutate(rows)
        checks.append((name, rows, True))
    results = []
    for name, rows, reject in checks:
        errors = acceptance_errors(rows, cases, old_failure)
        check(bool(errors) == reject, 'helper incorrect: ' + name)
        results.append(dict(case=name, rejected=bool(errors), errors=errors))
    check(acceptance_errors(base, ['positive', 'positive'], set()), 'duplicate case declaration accepted')
    check(acceptance_errors(base, cases, {'undeclared'}), 'unknown failure declaration accepted')
    results += [dict(case='duplicate-case-declaration', rejected=True),
                dict(case='undeclared-old-failure', rejected=True)]
    return results


def main():
    # Warm standard-library platform caches before the real-process tripwire.
    platform.platform()
    platform.machine()
    result = dict(scope='pure local runner-status tests; no native or vendor execution',
                  repaired=[], original_controls=[], helper=[])
    try:
        result['helper'] = helper_controls()
        for script in SPECS:
            for scenario in SCENARIOS:
                result['repaired'].append(exercise(script, scenario))
            for scenario in ['old-build-failure', 'wrong-candidate-exit', 'case-timeout']:
                result['original_controls'].append(exercise(script, scenario, original=True))
        before = json.loads((ROOT / 'frozen23-before.json').read_text())
        after = {str(p.relative_to(FROZEN)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(FROZEN.rglob('*')) if p.is_file()}
        check(before == after, 'frozen23 contents changed')
        result['frozen23_unchanged'] = True
        result['passed'] = True
    except Exception as error:
        result.update(passed=False, failure=dict(type=type(error).__name__, message=str(error)))
        raise
    finally:
        (ROOT / 'test-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS {} repaired runner executions; {} original false-zero controls; {} verdict controls; frozen23 unchanged'.format(
        len(result['repaired']), len(result['original_controls']), len(result['helper'])))


if __name__ == '__main__':
    main()
