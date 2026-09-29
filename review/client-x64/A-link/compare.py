from pathlib import Path
import struct,json,hashlib
root=Path(__file__).resolve().parent

def normalize(data):
    b=bytearray(data);pe=struct.unpack_from('<I',b,60)[0]
    assert b[pe:pe+4]==b'PE\0\0'
    op=pe+24;assert struct.unpack_from('<H',b,op)[0]==0x10b
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

before=(root/'product-before.exe').read_bytes();after=(root/'product-after.exe').read_bytes()
a,af,ah=normalize(before);b,bf,bh=normalize(after)
result={'normalized_equal':a==b,'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'before_bytes':len(before),'after_bytes':len(after),'before_normalized_fields':af,'after_normalized_fields':bf,'sections_equal':{s:ah[s]==bh.get(s) for s in ah},'diagnostic_markers_absent':all(x not in before and x not in after for x in [b'fpu-transition.log',b'fpu-runtime.log',b'collision-entry',b'dpvs-entry'])}
(root/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['normalized_equal'];assert result['diagnostic_markers_absent']
