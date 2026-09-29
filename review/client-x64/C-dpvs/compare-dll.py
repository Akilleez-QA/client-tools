from pathlib import Path
import struct,json,hashlib,re
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
        if typ==2 and b[ptr:ptr+4]==b'RSDS':fields.append((ptr+4,20,'PDB GUID and age'))
    # Normalize only source-identified build-date text and parsed CodeView path.
    for match in re.finditer(rb'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [ 0-9][0-9] [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\x00',b):
        fields.append((match.start(),len(match.group())-1,'DPVS_BUILD_TIME (__DATE__ __TIME__)'))
    for i in range(size//28):
        o=pos(rv)+28*i;typ=struct.unpack_from('<I',b,o+12)[0];ptr=struct.unpack_from('<I',b,o+24)[0]
        if typ==2 and b[ptr:ptr+4]==b'RSDS':
            end=b.index(0,ptr+24); path=bytes(b[ptr+24:end]); normalized=path.replace(b'\\Win32\\',b'\\win32\\')
            assert normalized.lower()==path.lower()
            b[ptr+24:end]=normalized
    for o,n,_ in fields:b[o:o+n]=b'\0'*n
    return b,fields,hashes


result={}
base=(root/'native/base-Win32-Release/dpvs.dll').read_bytes()
a,af,ah=normalize(base)
for variant in ['c1','c2']:
 data=(root/('native/'+variant+'-Win32-Release/dpvs.dll')).read_bytes()
 b,bf,bh=normalize(data)
 diffs=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
 result[variant]={'normalized_equal':a==b,'size_base':len(a),'size_candidate':len(b),'differing_bytes':len(diffs),'first_differences':diffs[:30],'normalized_fields':bf,'raw_sections_equal':{s:ah[s]==bh.get(s) for s in ah}}
(root/'dll-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
