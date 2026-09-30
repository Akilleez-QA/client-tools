from pathlib import Path
import re,hashlib,json,shutil
b=Path(__file__).resolve().parent;p=b.parent/'miles-rpc-contract'
(b/'prior-evidence-hashes.json').write_text(json.dumps({n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['PLAN.md','RESULTS.md','probe.cpp','run.py','analyze.py']},indent=2))
s=(p/'probe.cpp').read_text()
s=s.replace('struct Event {uint32_t sequence,id,op,thread,eos;', 'struct Event {uint32_t sequence,id,op,lastId,lastOp,thread,eos;')
s=s.replace('eosSequence,activeId,activeOp;', 'eosSequence,activeId,activeOp,lastId,lastOp;')
s=s.replace('e.op=activeOp;', 'e.op=activeOp;e.lastId=lastId;e.lastOp=lastOp;')
s=s.replace('static HSAMPLE sample;', 'static uint32_t vendorCalls,statusCalls,lifetime,creates,releases,starts;static bool bypass;\nstatic HSAMPLE sample;')
start=s.index('static Reply dispatch(');end=s.index('static bool send(',start)
old=s[start:end]
switch=old[old.index(' switch(r.op)'):old.index(' }record();return a;}')+2]
switch=switch.replace('case CREATE:','case CREATE:')
switch=switch.replace('}break;\n case START:', '}++creates;lifetime=generation;break;\n case START:')
switch=switch.replace('case START:', 'case START:++starts;')
switch=switch.replace('case STATUS:', 'case STATUS:++statusCalls;')
switch=switch.replace('sample=0;stream=0;++generation;', 'sample=0;stream=0;++releases;lifetime=0;++generation;')
# Count every genuine vendor call in dispatcher, including allocation/configuration/release.
switch=re.sub(r'p_(AIL_\w+)\(([^()]*)\)',r'(++vendorCalls,p_\1(\2))',switch)
s=s[:start]+'''static void audit(const char *phase,const Request &r){fprintf(stderr,"audit phase=%s id=%u op=%u request_gen=%u current_gen=%u handle=%p lifetime=%u vendor=%u statuscalls=%u creates=%u releases=%u starts=%u qpc=%I64d\\n",phase,r.id,r.op,r.generation,generation,sample?(void*)sample:(void*)stream,lifetime,vendorCalls,statusCalls,creates,releases,starts,tick());}
static Reply dispatch(const Request &r){Reply a={1,r.id,0,0,1,generation,0,-1,-1,-1};
 EnterCriticalSection(&gate);activeId=r.id;activeOp=r.op;lastId=r.id;lastOp=r.op;record();LeaveCriticalSection(&gate);audit("begin",r);
 if(r.version!=1||r.reserved||r.op<CREATE||r.op>QUIT)a.result=2;
 else if(r.op!=CREATE&&r.op!=QUIT&&(r.slot!=1||(!bypass&&r.generation!=generation)||(!sample&&!stream)))a.result=1;
 else {
'''+switch+'''
 }
 audit("end",r);EnterCriticalSection(&gate);record();activeId=activeOp=0;LeaveCriticalSection(&gate);return a;}
'''+s[end:]
s=s.replace('bool direct=!strcmp(argv[4],"direct");','bool direct=!strcmp(argv[4],"direct");bypass=!strcmp(argv[4],"mutant");')
s=s.replace('uint32_t tail[]={STOP,RELEASE,STATUS,QUIT};for(int i=0;i<4&&ok;++i){r.id++;r.op=tail[i];ok=execute(r,true);}', 'uint32_t tail[]={STOP,RELEASE,CREATE,STATUS,STATUS,RELEASE,QUIT};uint32_t gens[]={1,1,2,1,2,2,3};for(int i=0;i<7&&ok;++i){r.id++;r.op=tail[i];r.generation=gens[i];ok=execute(r,true);}')
s=s.replace('event seq=%u id=%u op=%u tid=', 'event seq=%u active_id=%u active_op=%u observed_last_id=%u observed_last_op=%u tid=')
s=s.replace('e.sequence,e.id,e.op,e.thread', 'e.sequence,e.id,e.op,e.lastId,e.lastOp,e.thread')
s=s.replace('generation=%u\\n",eventCount,eosCount,ok,generation', 'generation=%u creates=%u releases=%u starts=%u vendor=%u statuscalls=%u live=%u bypass=%u\\n",eventCount,eosCount,ok,generation,creates,releases,starts,vendorCalls,statusCalls,(sample||stream)?1:0,bypass')
s=s.replace('eosCount==1&&generation==2', 'eosCount==1&&generation==3&&creates==2&&releases==2&&starts==1')
# Controller argv gains explicit guard variant; keep receiving and cleanup on expected stale acceptance.
s=s.replace('int main(int argc,char **argv){if(argc!=5)return 2;LARGE_INTEGER', 'int main(int argc,char **argv){if(argc!=6)return 2;LARGE_INTEGER')
s=s.replace('%s controlled",argv[1],argv[2],argv[3],argv[4]', '%s %s",argv[1],argv[2],argv[3],argv[4],argv[5]')
s=s.replace('uint32_t ops[66]', 'bool oracle=true;uint32_t ops[69]')
s=s.replace('ops[count++]=RELEASE;ops[count++]=STATUS;ops[count++]=QUIT;', 'ops[count++]=RELEASE;ops[count++]=CREATE;ops[count++]=STATUS;ops[count++]=STATUS;ops[count++]=RELEASE;ops[count++]=QUIT;')
s=s.replace('Request r={1,++id,ops[i],1,1,0};', 'uint32_t gen=i==64||i==66||i==67?2u:(i==68?3u:1u);Request r={1,++id,ops[i],1,gen,0};printf("request id=%u op=%u generation=%u\\n",r.id,r.op,r.generation);fflush(stdout);')
s=s.replace('if(a.kind!=0||a.result!=(i==64?1u:0u)){ok=false;}', 'if(a.kind!=0){ok=false;}if(a.result!=(i==65?1u:0u)){oracle=false;}')
s=s.replace('host_exit=%lu ok=%d\\n",replies,events,code,ok', 'host_exit=%lu ok=%d oracle=%d\\n",replies,events,code,ok,oracle')
s=s.replace('ok&&code==0&&events==1&&replies==66', 'ok&&oracle&&code==0&&events==1&&replies==69')
(b/'probe.cpp').write_text(s)
shutil.copy2(p/'Mss.h',b/'Mss.h');shutil.copy2(p/'build.cmd',b/'build.cmd')
