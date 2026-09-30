from pathlib import Path
import hashlib,json
from symbol_parser import undefined_symbols,has_required,no_miles_imports
D=Path(__file__).resolve().parent
log=D.parent/'native39-owner/native-evidence-v1/curated/results/owner/symbols.log'
s=log.read_text();prefix='?enqueueAdmitted@FileInvocationJob@MilesFileExecutor30@@'
actual=undefined_symbols(s);line=next(x for x in s.splitlines() if 'UNDEF' in x and prefix in x)
checks={'actual_expected_present':has_required(actual,[prefix]),'actual_no_sdk':no_miles_imports(actual),
 'absent_rejected':not has_required(undefined_symbols(s.replace(line,'')),[prefix]),
 'defined_only_rejected':not has_required(undefined_symbols(line.replace('UNDEF','SECT123')),[prefix]),
 'sdk_mutation_rejected':not no_miles_imports(undefined_symbols(s+'\n000 UNDEF External | __imp_AIL_open_stream (native)\n')),
 'demangled_suffix_ignored':undefined_symbols(line)==[line.split('|',1)[1].strip().split()[0]]}
assert all(checks.values()),checks
out=D/'parser-checks.json';assert not out.exists()
out.write_text(json.dumps({'actual_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'checks':checks},indent=2)+'\n');print(json.dumps(checks))
