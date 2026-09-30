"""Acceptance for the declared two-variant matrix, derived from raw exit records."""
from collections import Counter


def acceptance_errors(records, cases, old_failure):
    """Return diagnostics; an empty list is the only passing verdict.

    Each variant needs exactly one successful build and one result per case.
    Negative-control expectations come from the declared case set, never from
    a record's `expected` or `matches` fields. Present metadata must agree.
    """
    if (not cases or any(not isinstance(case, str) or not case for case in cases)
            or len(set(cases)) != len(cases)):
        return ['case declaration must contain distinct nonempty names']
    if not set(old_failure).issubset(cases):
        return ['old failure declaration contains an undeclared case']
    if not isinstance(records, list):
        return ['results must be a list']

    expected = {}
    for variant in ('old', 'candidate'):
        expected[(variant, 'build', None)] = 0
        for case in cases:
            expected[(variant, 'case', case)] = int(variant == 'old' and case in old_failure)
    seen = Counter()
    errors = []
    for index, record in enumerate(records):
        label = 'record {}'.format(index)
        if not isinstance(record, dict):
            errors.append(label + ': not an object')
            continue
        variant = record.get('variant')
        if variant not in ('old', 'candidate'):
            errors.append(label + ': unknown variant')
            continue
        if record.get('stage') == 'build' and 'case' not in record:
            key = (variant, 'build', None)
        elif 'stage' not in record and isinstance(record.get('case'), str):
            key = (variant, 'case', record['case'])
        else:
            errors.append(label + ': unknown or ambiguous result shape')
            continue
        if key not in expected:
            errors.append(label + ': undeclared case')
            continue
        seen[key] += 1
        label = '{} {}'.format(variant, key[2] if key[1] == 'case' else 'build')
        wanted = expected[key]
        if 'timeout' in record and record['timeout'] is not False:
            errors.append(label + ': timeout or invalid timeout flag')
        actual = record.get('exit')
        matches = type(actual) is int and actual == wanted
        if not matches:
            errors.append('{}: expected exit {}, got {!r}'.format(label, wanted, actual))
        if 'expected' in record and (type(record['expected']) is not int or record['expected'] != wanted):
            errors.append(label + ': reported expected exit contradicts declaration')
        if 'matches' in record and (type(record['matches']) is not bool or record['matches'] != matches):
            errors.append(label + ': reported matches contradicts raw exit/declaration')
    for key in expected:
        if seen[key] != 1:
            label = '{} {}'.format(key[0], key[2] if key[1] == 'case' else 'build')
            errors.append('{}: expected one record, got {}'.format(label, seen[key]))
    return errors
