"""Strict negative-control diagnostics; unrelated build failures are failures."""
import ntpath
import re


def key(path):
    return ntpath.normcase(ntpath.normpath(str(path)))


def expected_failure(text, allowed):
    """allowed maps exact source paths to (line or None, code, message regex)."""
    allowed = {key(path): rules for path, rules in allowed.items()}
    found = 0
    for line in text.splitlines():
        if not re.search(r'\b(?:fatal\s+)?error\b|not recognized|cannot find', line, re.I):
            continue
        match = re.match(r'^(.*?)\((\d+)(?:,\d+)?\)\s*:\s*(?:fatal )?error (C\d+):\s*(.*)$', line)
        if not match:
            return False
        path, number, code, message = match.groups()
        if not any((at is None or at == int(number)) and code == wanted and re.fullmatch(cause, message)
                   for at, wanted, cause in allowed.get(key(path), ())):
            return False
        found += 1
    return found > 0
