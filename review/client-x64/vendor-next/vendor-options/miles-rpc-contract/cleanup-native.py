from pathlib import Path
import shutil
p=Path('C:/miles-rpc-contract-private')
assert p.name=='miles-rpc-contract-private' and p.parent==Path('C:/')
shutil.rmtree(p)
print('owned_native_scratch_exists='+str(p.exists()))
