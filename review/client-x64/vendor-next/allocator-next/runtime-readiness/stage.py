from pathlib import Path
import shutil,json,hashlib,struct,ctypes,subprocess,os,re
root=Path('C:/integration-current-v2/workspace/repo');out=Path('C:/runtime-staging49d0-v1');out.mkdir(exist_ok=False)
rows=[]
def info(p):
 b=p.read_bytes();off=struct.unpack_from('<I',b,60)[0];return {'sha256':hashlib.sha256(b).hexdigest(),'machine':hex(struct.unpack_from('<H',b,off+4)[0]),'bytes':len(b)}
for cfg,suffix in [('Release','r'),('Debug','d')]:
 d=out/cfg;d.mkdir();sources=[root/'src/compile/x64'/proj/cfg/('gl'+number+'_'+suffix+'.dll') for proj,number in [('Direct3d9','05'),('Direct3d9_ffp','06'),('Direct3d9_vsps','07')]]
 sources.extend([root/'src/compile/x64/dpvs'/cfg/'dpvs.dll',root/'src/compile/deps/parsers-v120/x64'/cfg/'libxml2.dll',Path('C:/runtime-readiness-private-directx/runtime-x64/d3dx9_43.dll')])
 for source in sources:
  before=info(source);assert before['machine']=='0x8664';dest=d/source.name;shutil.copy2(source,dest);assert info(dest)==before;rows.append(dict(configuration=cfg,source=str(source),destination=str(dest),**before))
 assert not (d/'DllExport.dll').exists()
(out/'staging-manifest.json').write_text(json.dumps({'source_head':'49d0eeed4ddaa177d7a93ea396c37c3d9b9942da','private_only':True,'no_client_executable':True,'files':rows},indent=2))
# Only libraries without game-host imports: no renderer or game executable is loaded.
k=ctypes.WinDLL('kernel32',use_last_error=True);k.LoadLibraryExW.argtypes=[ctypes.c_wchar_p,ctypes.c_void_p,ctypes.c_uint];k.LoadLibraryExW.restype=ctypes.c_void_p;k.GetProcAddress.argtypes=[ctypes.c_void_p,ctypes.c_char_p];k.GetProcAddress.restype=ctypes.c_void_p;k.FreeLibrary.argtypes=[ctypes.c_void_p];k.FreeLibrary.restype=ctypes.c_int
checks=[]
for cfg in ['Release','Debug']:
 for name in ['d3dx9_43.dll','dpvs.dll','libxml2.dll']:
  p=out/cfg/name;h=k.LoadLibraryExW(str(p),None,0x00000100|0x00001000);row={'configuration':cfg,'library':name,'loaded':bool(h),'error':ctypes.get_last_error() if not h else 0}
  if h and name=='d3dx9_43.dll':
   a=k.GetProcAddress(h,b'D3DXCheckVersion');row['D3DXCheckVersion_export']=bool(a);row['version_matches_sdk32_d3dx43']=bool(ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_uint,ctypes.c_uint)(a)(32,43)) if a else False
  if h:row['freed']=bool(k.FreeLibrary(h))
  checks.append(row)
(out/'loader-checks.json').write_text(json.dumps({'python_bits':struct.calcsize('P')*8,'scope':'LoadLibraryEx/FreeLibrary only; D3DX version query; no game/renderer/DPVS initialization or device creation','checks':checks},indent=2));print(checks)
