#include "clientAudio/FirstClientAudio.h"
#include "clientAudio/SetupClientAudio.h"
#include "clientAudio/Audio.h"
#include "clientAudio/Sound2.h"
#include "clientAudio/Sound2dTemplate.h"
#include "sharedFoundation/SetupSharedFoundation.h"
#include "sharedFile/SetupSharedFile.h"
#include "sharedFile/Iff.h"
#include "sharedThread/SetupSharedThread.h"
#include "sharedDebug/SetupSharedDebug.h"
#include "sharedMath/SetupSharedMath.h"
#include "sharedRandom/SetupSharedRandom.h"
#include "sharedUtility/SetupSharedUtility.h"
#include <windows.h>
#include <stdio.h>
#if _MSC_VER != 1800 || defined(_WIN64)
#error Native v120 Win32 baseline required
#endif
static volatile LONG completions;
static LONG CALLBACK traceException(EXCEPTION_POINTERS* e){if(e->ExceptionRecord->ExceptionCode==0xc0000005){printf("NATIVE_EXCEPTION code=%08lx address=%p base=%p\n",e->ExceptionRecord->ExceptionCode,e->ExceptionRecord->ExceptionAddress,GetModuleHandle(0));void* stack[32];USHORT count=CaptureStackBackTrace(0,32,stack,0);for(USHORT i=0;i<count;++i)printf("FRAME %p\n",stack[i]);}return EXCEPTION_CONTINUE_SEARCH;}
static void completed(){LARGE_INTEGER q;QueryPerformanceCounter(&q);InterlockedIncrement(&completions);printf("ENGINE_CALLBACK count=%ld qpc=%I64d tid=%lu\n",completions,q.QuadPart,GetCurrentThreadId());}
int main(int argc,char **argv){
 setvbuf(stdout,0,_IONBF,0);AddVectoredExceptionHandler(1,traceException);if(argc!=1)return 2;
 puts("stage thread");SetupSharedThread::install();SetupSharedDebug::install(4096);
 SetupSharedFoundation::Data data(SetupSharedFoundation::Data::D_console);data.writeMiniDumps=false;data.configFile="probe.cfg";data.argc=argc;data.argv=argv;
 puts("stage foundation");SetupSharedFoundation::install(data);
 puts("stage file");SetupSharedFile::install(false,0);
 puts("stage math");SetupSharedMath::install();
 SetupSharedUtility::Data util;SetupSharedUtility::setupToolData(util);util.m_allowFileCaching=true;SetupSharedUtility::install(util);
 SetupSharedRandom::install(12345);
 puts("stage audio");SetupClientAudio::install();
 {Sound2dTemplate t;t.setLoopCountMin(2);t.setLoopCountMax(2);t.setAttenuationMethod(Audio::AM_none);t.setSoundCategory(Audio::SC_userInterface);t.addSample("sample.wav",true);t.addSample("second.wav",true);Iff iff(2048);t.write(iff);if(!iff.write("probe.snd"))return 3;}
 puts("stage play");SoundId id=Audio::playSound("probe.snd");Audio::setEndOfSampleCallBack(id,completed);
 for(int i=0;i<100;++i){Audio::alter(i==0?0.0f:0.01f,0);Audio::serve();Sound2*sound=Audio::getSoundById(id);int total=-1,current=-1;bool timeValid=Audio::getCurrentSoundTime(id,total,current);printf("ALTER epoch=%d sound=%d sample=%d timeValid=%d total=%d current=%d eos=%ld\n",i,sound!=0,sound?sound->getSampleId().getId():0,timeValid,total,current,completions);if(i==40){puts("ALTER_ZERO");Audio::alter(0.0f,0);}Sleep(10);}
 bool released=!Audio::isSoundValid(id);printf("SUMMARY eos=%ld released=%d sounds=%d\n",completions,released,Audio::getSoundCount());puts("stage remove");SetupSharedFoundation::remove();puts("REMOVED");return completions==2&&released?0:4;
}
