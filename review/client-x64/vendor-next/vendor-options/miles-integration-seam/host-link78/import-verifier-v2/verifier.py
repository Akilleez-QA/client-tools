"""Strict parser for the observed dumpbin12 named-import group format."""
import re
DLL=re.compile(r'^\s{4}([A-Za-z0-9_.-]+\.dll)\s*$',re.I)
ROW=re.compile(r'^\s+([0-9A-Fa-f]+)\s+(\S+)\s*$')
META=re.compile(r'^\s+[0-9A-Fa-f]+ (?:Import Address Table|Import Name Table|time date stamp|Index of first forwarder reference)\s*$')
AIL=re.compile(r'^_AIL_[A-Za-z0-9_]+@[0-9]+$')
def verify(text,expected,dll='mss32.dll'):
    expected=set(expected)
    if not expected or any(not AIL.fullmatch(x) for x in expected):
        raise ValueError('Invalid expected decorated imports')
    groups={}; current=None; ended=False
    for line in text.splitlines():
        match=DLL.fullmatch(line)
        if match:
            if ended:raise ValueError('DLL after summary')
            current=match.group(1).lower()
            if current in groups:raise ValueError('Duplicate DLL group')
            groups[current]=[];continue
        if line.strip()=='Summary':current=None;ended=True;continue
        if current is None:continue
        if not line.strip() or META.fullmatch(line):continue
        match=ROW.fullmatch(line)
        if not match:raise ValueError('Unrecognized import-group line')
        token=match.group(2)
        if token in groups[current]:raise ValueError('Duplicate import')
        groups[current].append(token)
    if not ended or dll.lower() not in groups:raise ValueError('Missing DLL group or summary')
    actual=groups[dll.lower()]
    if any(not AIL.fullmatch(x) for x in actual) or set(actual)!=expected:
        raise ValueError('Exact decorated Miles imports differ')
    for name,tokens in groups.items():
        if name!=dll.lower() and any(AIL.fullmatch(x) for x in tokens):
            raise ValueError('Miles import in wrong DLL group')
    return sorted(actual)
