from pathlib import Path
import json,hashlib,struct
p=Path(__file__).resolve().parent; root=p.parent
b=(root/'private/public-sample/logo_legal.bik').read_bytes()
h=struct.unpack('<4s10I',b[:44]); assert len(b)==h[1]+8 and len(b)<1048576
assert h[5:7]==(640,480) and h[10]==0
(p/'asset.json').write_text(json.dumps(dict(url='https://samples.ffmpeg.org/game-formats/bink/logo_legal.bik',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),container='Bink',version=h[0].decode(),frames=h[2],width=h[5],height=h[6],rate=h[7],rate_div=h[8],flags=h[9],tracks=h[10],scope='Public non-SWG codec/IPC feasibility only'),indent=2))
s=(root/'probe.cpp').read_text().replace('#include <vector>','#include <vector>\n#include <io.h>\n#include <fcntl.h>')
s=s.replace(' SetErrorMode(', ' _setmode(_fileno(stdout),_O_BINARY);\n SetErrorMode(')
s=s.replace(' if(argc<2)', ' if(argc<2)')
a=s.index(' HBINKTRACK t='); z=s.index(' for(unsigned f=',a)
s=s[:a]+' // This bounded public sample has zero tracks; audio extraction is not exercised.\n if(b->NumTracks!=0){puts("{\\"error\\":\\"unexpected_audio_track_not_tested\\"}");pBinkClose(b);return 11;}\n'+s[z:]
a=s.index('  if(t){U32 n=');z=s.index('  if(f==1',a);s=s[:a]+s[z:]
a=s.index('char path[100];',s.index('  if(f==1'));z=s.index('\n  if(f<32',a)
s=s[:a]+'''printf("{\\"kind\\":\\"pixels\\",\\"frame\\":%u,\\"copy_status\\":%ld,\\"length\\":%u}\\n",f,copy,unsigned(pixels.size()));if(fwrite(pixels.data(),1,pixels.size(),stdout)!=pixels.size())return 8;putchar('\\n');}
'''+s[z:]
s=s.replace(' if(t)pBinkCloseTrack(t);pBinkClose(b);',' pBinkClose(b);')
(p/'probe-public.cpp').write_text(s)
s=(root/'driver.cpp').read_text().replace('probe32.exe','probe-public32.exe C:\\\\vendor-bink-probe\\\\public-sample\\\\logo_legal.bik').replace('data.size()>65536','data.size()>40*1024*1024').replace('BINKPROBE/1','BINKPUBLIC/1')
(p/'driver-public.cpp').write_text(s)
s=(root/'build.cmd').read_text().replace('probe.cpp','public-sample\\probe-public.cpp').replace('probe32.exe','public-sample\\probe-public32.exe').replace('driver.cpp','public-sample\\driver-public.cpp').replace('driver64.exe','public-sample\\driver-public64.exe')
# Driver launches child at the public experiment path, keeps original artifacts untouched.
d=(p/'driver-public.cpp').read_text().replace('\\\\probe-public32.exe','\\\\public-sample\\\\probe-public32.exe')
(p/'driver-public.cpp').write_text(d)
s=s.replace('/Fe:', '/Fo:public-sample\\ /Fe:')
(p/'build-public.cmd').write_text(s)
