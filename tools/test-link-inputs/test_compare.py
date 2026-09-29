from pathlib import Path
import struct, subprocess, json, argparse, sys
p=argparse.ArgumentParser(description='Negative controls for PE metadata normalization')
p.add_argument('--output',type=Path,required=True)
out=p.parse_args().output
out.mkdir(parents=True,exist_ok=False)
compare=str(Path(__file__).with_name('compare.py'))
b=bytearray(1024);b[:2]=b'MZ';struct.pack_into('<I',b,60,128);b[128:132]=b'PE\0\0';struct.pack_into('<HH',b,132,0x14c,1);struct.pack_into('<H',b,148,224);o=152;struct.pack_into('<H',b,o,0x10b);struct.pack_into('<I',b,o+60,512);struct.pack_into('<I',b,o+92,16);struct.pack_into('<II',b,o+96+48,0x1020,28);s=o+224;b[s:s+8]=b'.rdata\0\0';struct.pack_into('<IIII',b,s+8,512,4096,512,512);struct.pack_into('<I',b,s+36,0x40000040);struct.pack_into('<III',b,0x220+12,2,32,0x1080);struct.pack_into('<I',b,0x220+24,0x280);b[0x280:0x284]=b'RSDS';b[0x294:0x298]=b'AAAA';b[0x298:0x29e]=b'x.pdb\0'
results=[]
def check(name,left,right,want):
 (out/(name+'-before.exe')).write_bytes(left);(out/(name+'-after.exe')).write_bytes(right)
 r=subprocess.run([sys.executable,compare,str(out/(name+'-before.exe')),str(out/(name+'-after.exe')),'--output',str(out/(name+'.json'))],capture_output=True,text=True)
 (out/(name+'.log')).write_text(r.stdout+r.stderr)
 if (r.returncode==0)!=want: raise RuntimeError((name,r.stdout,r.stderr))
 results.append({'case':name,'exit':r.returncode,'expected_accept':want})
c=bytearray(b);c[0x294:0x298]=b'BBBB';check('metadata-only',b,c,True)
c=bytearray(b);c[0x310]=1;check('nonmetadata-data-change',b,c,False)
c=bytearray(b);c[s:s+8]=b'.text\0\0\0';struct.pack_into('<I',c,s+36,0x60000020);d=bytearray(c);d[0x294:0x298]=b'BBBB';check('code-masking',c,d,False)
c=bytearray(b);struct.pack_into('<I',c,s+16,1024);check('raw-outside-file',c,c,False)
c=bytearray(b);struct.pack_into('<H',c,134,2);c[s+40:s+80]=c[s:s+40];c[s+40:s+48]=b'.other\0\0';struct.pack_into('<I',c,s+52,8192);check('overlapping-sections',c,c,False)
c=bytearray(b);struct.pack_into('<I',c,o+96+52,29);check('partial-debug-entry',c,c,False)
c=bytearray(b);struct.pack_into('<I',c,0x220+24,0x290);check('rva-pointer-disagreement',c,c,False)
c=bytearray(b);struct.pack_into('<I',c,0x220+16,24);check('truncated-rsds',c,c,False)
c=bytearray(b);struct.pack_into('<I',c,o+96+48,0x11ff);check('directory-overrun',c,c,False)
check('truncated-file',b[:100],b[:100],False)
(out/'controls-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
