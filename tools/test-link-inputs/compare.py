from pathlib import Path
import struct,json,hashlib
import argparse
p=argparse.ArgumentParser(description="Compare Win32 PE files, normalizing only timestamps and PDB age")
p.add_argument('before',type=Path);p.add_argument('after',type=Path);p.add_argument('--output',type=Path,required=True)
a=p.parse_args()

def normalize(data):
    b=bytearray(data);pe=struct.unpack_from('<I',b,60)[0]
    if b[pe:pe+4] != b'PE\0\0': raise ValueError('not a PE image')
    op=pe+24
    if struct.unpack_from('<H',b,op)[0] != 0x10b: raise ValueError('expected Win32 PE')
    dd=op+96;num=struct.unpack_from('<H',b,pe+6)[0]
    sh=op+struct.unpack_from('<H',b,pe+20)[0];sections=[];hashes={}
    for i in range(num):
        o=sh+40*i;name=b[o:o+8].rstrip(b'\0').decode()
        vs,va,rs,rp=struct.unpack_from('<IIII',b,o+8)
        sections.append((va,max(vs,rs),rp));hashes[name]=hashlib.sha256(b[rp:rp+rs]).hexdigest()
    def pos(rva):
        for va,size,rp in sections:
            if va<=rva<va+size:return rp+rva-va
        raise ValueError(rva)
    fields=[(pe+8,4,'COFF timestamp')]
    exp=struct.unpack_from('<I',b,dd)[0]
    if exp:fields.append((pos(exp)+4,4,'export timestamp'))
    rv,size=struct.unpack_from('<II',b,dd+6*8)
    for i in range(size//28):
        o=pos(rv)+28*i;fields.append((o+4,4,'debug timestamp'))
        typ=struct.unpack_from('<I',b,o+12)[0];ptr=struct.unpack_from('<I',b,o+24)[0]
        if typ==2 and b[ptr:ptr+4]==b'RSDS':fields.append((ptr+20,4,'PDB age'))
    for o,n,_ in fields:b[o:o+n]=b'\0'*n
    return b,fields,hashes

before=a.before.read_bytes();after=a.after.read_bytes();output=a.output
a,af,ah=normalize(before);b,bf,bh=normalize(after)
result={'normalized_equal':a==b,'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'before_bytes':len(before),'after_bytes':len(after),'before_normalized_fields':af,'after_normalized_fields':bf,'sections_equal':{s:ah[s]==bh.get(s) for s in ah},'diagnostic_markers_absent':all(x not in before and x not in after for x in [b'fpu-transition.log',b'fpu-runtime.log',b'collision-entry',b'dpvs-entry'])}
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['normalized_equal'] and result['diagnostic_markers_absent'] else 1)
