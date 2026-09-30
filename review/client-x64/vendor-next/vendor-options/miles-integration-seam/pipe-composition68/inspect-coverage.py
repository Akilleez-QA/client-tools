#!/usr/bin/env python3
"""Source inventory only. Not a C++ parser, compiler, linker or ABI check."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def stripped(path):
    text = path.read_text()
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)

RET = r'(void|int32_t|uint32_t|intptr_t|HDIGDRIVER|HSAMPLE|HSTREAM|SampleCallback|StreamCallback|const\s+char\s*\*)'

def inventory(text, ending):
    found = {}
    for match in re.finditer(r'^\s*' + RET + r'\s*(\w+)\s*\(([^)]*)\)\s*' + ending, text, re.M):
        ret, name, args = match.groups()
        if name in found:
            raise ValueError('duplicate lexical name: ' + name)
        types = []
        for arg in args.split(',') if args.strip() else []:
            arg = arg.strip()
            # This fixed header uses only scalar/pointer arguments, with no
            # arrays, default arguments, function-pointer declarators or templates.
            tokens = re.findall(r'\w+|\*', arg)
            if len(tokens) > 1 and tokens[-1] != '*' and tokens[-1] not in ['void', 'char']:
                tokens.pop()  # Named parameter; unnamed opaque types are one token.
            types.append(' '.join(tokens))
        found[name] = {'return': ' '.join(re.findall(r'\w+|\*', ret)), 'parameters': types}
    return found

public = inventory(stripped(ROOT / 'candidate/backend-boundary24/ClientMiles.h'), ';')
exports = inventory(stripped(ROOT / 'candidate/backend-boundary24/pipe/ClientMilesPipe.cpp').split('namespace ClientMiles {', 1)[1], r'\{')
core_text = stripped(ROOT / 'candidate/backend-boundary24/pipe/PipeCore.cpp').split('namespace ClientMilesPipeCore57 {', 1)[1]
core = inventory(core_text, r'\{')
rows = []
for name, signature in public.items():
    exported = name in exports
    same = exported and all(signature[k] == exports[name][k] for k in ['return', 'parameters'])
    core_same = exported and name in core and all(exports[name][k] == core[name][k] for k in ['return', 'parameters'])
    rows.append({'name': name, 'public_signature': signature, 'exported': exported,
                 'lexical_signature_equal': same if exported else None,
                 'real_core_definition_lexically_equal': core_same if exported else None})
result = {'method': 'Restricted lexical inventory plus human source review; NOT compilation/link/ABI proof',
          'declared_count': len(public), 'defined_count': len(exports),
          'unresolved': sorted(set(public) - set(exports)),
          'unexpected_exports': sorted(set(exports) - set(public)), 'operations': rows}
if result['unexpected_exports'] or any(r['exported'] and not (r['lexical_signature_equal'] and r['real_core_definition_lexically_equal']) for r in rows):
    raise ValueError('source inventory mismatch')
(ROOT / 'coverage.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['method', 'declared_count', 'defined_count', 'unresolved']}))
