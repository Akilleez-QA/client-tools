from pathlib import Path
import subprocess,re,json,hashlib,xml.etree.ElementTree as ET
out=Path('C:/null-realloc-compile-v1');out.mkdir();inputs=Path('C:/null-realloc-input');results=[]
q=lambda p:'"'+str(p)+'"'
for config in ['Debug','Release']:
 for platform,arch in [('win32','x86'),('x64','x86_amd64')]:
  repo=Path('C:/integration-current-v1/workspace/repo' if platform=='win32' else 'C:/integration-current-v2/workspace/repo')
  for library,name in [('sharedMemoryManager','MemoryManager.cpp'),('sharedXml','SetupSharedXml.cpp'),('sharedDatabaseInterface','OciSession.cpp')]:
   project=repo/'src/engine/shared/library'/library/'build/win32'
   base=inputs/name
   for variant in (['normal','tracked-guards'] if name=='MemoryManager.cpp' else ['normal']):
    d=out/(config+'-'+platform)/library/variant;d.mkdir(parents=True)
    result=dict(configuration=config,platform=platform,source=name,variant=variant);results.append(result)
    try:
     if library=='sharedDatabaseInterface':
      tree=ET.parse(project/(library+'.vcxproj'));ns={'m':'http://schemas.microsoft.com/developer/msbuild/2003'}
      group=next(g for g in tree.findall('m:ItemDefinitionGroup',ns) if "'"+config+'|Win32' + "'" in g.attrib.get('Condition',''))
      cl=group.find('m:ClCompile',ns);defs=cl.find('m:PreprocessorDefinitions',ns).text.split(';');incs=cl.find('m:AdditionalIncludeDirectories',ns).text.split(';')
      defs=[v for v in defs if v and not v.startswith('%') and not(platform=='x64' and v.startswith('_USE_32BIT_TIME_T'))]
      cmd=' '.join(['/c','/nologo','/EHsc','/Zc:wchar_t-','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']+['/D'+q(v) for v in defs]+['/I'+q(v) for v in incs if v and not v.startswith('%')])
      result['metadata']='Actual Win32 project properties; x64 diagnostic compiler adaptation drops _USE_32BIT_TIME_T only'
     else:
      logs=list((repo/'src/compile'/platform/library/config).rglob('cl.command.1.tlog'));assert len(logs)==1
      lines=logs[0].read_text(encoding='utf-16').splitlines();cmd=next(lines[i+1] for i,l in enumerate(lines) if l.startswith('^') and l.upper().endswith(name.upper()))
      cmd=re.sub(r'(?i)[QR]:\\REPO\\\S*'+re.escape(name),'',cmd)
      for flag in ['Fo','Fd','Fp','Yu']:
       cmd=re.sub(r'(?i)/'+flag+r'(?:"[^"]*"|\S+)','',cmd)
      cmd=re.sub(r'(?i)/Gm\b','/Gm-',cmd)
     text=base.read_text()
     if variant=='tracked-guards':
      for key,value in [('DO_TRACK','5'),('DO_SCALAR','1'),('DO_GUARDS','1')]:text,n=re.subn(r'(#define '+key+r' +)0',lambda m:m[1]+value,text,count=1);assert n==1
     source=d/name;source.write_text(text);result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
     cmd+=' /Y- /I'+q(repo/'src/engine/shared/library'/library/'src_oci')+' /c '+q(source)+' /Fo'+q(d/'source.obj')+' /Fd'+q(d/'source.pdb')
     (d/'compile.rsp').write_text(cmd)
     bat=d/'compile.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncl @'+q(d/'compile.rsp')+'\nexit /b %errorlevel%\n')
     p=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(d/'compile.log').write_bytes(p.stdout);result['compile_exit']=p.returncode
    except Exception as e:result['error']=str(e)
    (out/'results.json').write_text(json.dumps(results,indent=2));print(result,flush=True)
