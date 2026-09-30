#if _MSC_VER != 1800
#error Native evidence requires v120
#endif
// Build with /DWIN32 /EHsc and checkout src on the include path.
// Runtime covers actual trylock/unlock only. The test drives retries itself.
// Production lock()/yield_thread() runtime remains unverified.
// Native Win32 and x64; run each process with an outer timeout as well.
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#include <process.h>
#include <stdio.h>
#include <stdlib.h>
#include "engine/shared/library/sharedFoundationTypes/include/public/sharedFoundationTypes/FoundationTypes.h"
#include "VeCritsec.hpp"

static_assert(sizeof(long) == 4, "Windows interlocked operand is 32 bits");
static_assert(sizeof(VeCritsec) == 12, "lock layout changed");
static_assert(__alignof(VeCritsec) == 4, "lock alignment changed");
static unsigned checks = 0;
static void require(bool value, char const *name)
{
    if (!value) { fprintf(stderr, "FAIL %s error=%lu\n", name, GetLastError()); fflush(stderr); ExitProcess(1); }
    ++checks; printf("PASS %s\n", name); fflush(stdout);
}
static void waitFor(HANDLE handle, char const *name)
{
    require(WaitForSingleObject(handle, 10000) == WAIT_OBJECT_0, name);
}
static HANDLE eventHandle()
{
    HANDLE event = CreateEvent(NULL, FALSE, FALSE, NULL);
    if (!event) { fprintf(stderr, "event creation failed\n"); ExitProcess(1); }
    return event;
}
static void acquireForProbe(VeCritsec &lock)
{
    while (!lock.trylock()) SwitchToThread();
}
struct Ownership
{
    VeCritsec lock;
    HANDLE request, reply, enterBlocking, entered;
    volatile LONG acquired;
    Ownership() : request(eventHandle()), reply(eventHandle()), enterBlocking(eventHandle()), entered(eventHandle()), acquired(-1) {}
};
static unsigned __stdcall ownerWorker(void *opaque)
{
    Ownership &s = *static_cast<Ownership *>(opaque);
    for (int phase = 0; phase < 2; ++phase)
    {
        if (WaitForSingleObject(s.request, 10000) != WAIT_OBJECT_0) return 1;
        bool acquired = s.lock.trylock();
        InterlockedExchange(&s.acquired, acquired ? 1 : 0);
        if (acquired) s.lock.unlock();
        SetEvent(s.reply);
    }
    SetEvent(s.enterBlocking);
    acquireForProbe(s.lock);
    SetEvent(s.entered);
    s.lock.unlock();
    return 0;
}
static void join(HANDLE thread, char const *name)
{
    waitFor(thread, name);
    DWORD code = 1;
    require(GetExitCodeThread(thread, &code) && code == 0, "worker exit code");
    CloseHandle(thread);
}
static void ownership()
{
    Ownership s;
    require(s.lock.trylock(), "initial acquisition");
    require(s.lock.trylock(), "recursive acquisition");
    HANDLE thread = reinterpret_cast<HANDLE>(_beginthreadex(NULL, 0, ownerWorker, &s, 0, NULL));
    require(thread != NULL, "ownership worker created");
    SetEvent(s.request); waitFor(s.reply, "first competing attempt completed");
    require(InterlockedCompareExchange(&s.acquired, -1, -1) == 0, "other thread excluded while nested");
    s.lock.unlock();
    SetEvent(s.request); waitFor(s.reply, "second competing attempt completed");
    require(InterlockedCompareExchange(&s.acquired, -1, -1) == 0, "one unlock does not release nested owner");
    waitFor(s.enterBlocking, "worker ready for retry acquisition");
    s.lock.unlock();
    waitFor(s.entered, "final unlock permits retry acquisition");
    join(thread, "ownership worker joined");
    require(s.lock.trylock(), "lock reusable after transfer");
    s.lock.unlock();
    CloseHandle(s.request); CloseHandle(s.reply); CloseHandle(s.enterBlocking); CloseHandle(s.entered);
}
struct Stress
{
    VeCritsec lock;
    HANDLE start;
    unsigned count, inverse;
    volatile LONG failed;
    Stress() : start(CreateEvent(NULL, TRUE, FALSE, NULL)), count(0), inverse(~0u), failed(0) {}
};
static unsigned __stdcall stressWorker(void *opaque)
{
    Stress &s = *static_cast<Stress *>(opaque);
    if (WaitForSingleObject(s.start, 10000) != WAIT_OBJECT_0) return 1;
    for (unsigned n = 0; n < 25000; ++n)
    {
        acquireForProbe(s.lock);
        acquireForProbe(s.lock);
        if (s.inverse != ~s.count) InterlockedExchange(&s.failed, 1);
        unsigned next = s.count + 1;
        // Yield while owning the lock: make contention likely, never use this
        // as a timing oracle. Deterministic exclusion was checked above.
        if ((n & 255) == 0) SwitchToThread();
        s.count = next;
        s.inverse = ~next;
        s.lock.unlock();
        s.lock.unlock();
    }
    return 0;
}
static void stress()
{
    Stress s;
    require(s.start != NULL, "stress event created");
    HANDLE threads[4];
    for (unsigned i = 0; i < 4; ++i)
    {
        threads[i] = reinterpret_cast<HANDLE>(_beginthreadex(NULL, 0, stressWorker, &s, 0, NULL));
        require(threads[i] != NULL, "stress worker created");
    }
    SetEvent(s.start);
    for (unsigned i = 0; i < 4; ++i) join(threads[i], "stress worker joined");
    require(s.failed == 0, "protected payload stays coherent");
    require(s.count == 100000 && s.inverse == ~100000u, "exact protected update total");
    CloseHandle(s.start);
}
int main()
{
    ownership();
    stress();
    if (checks != 27) { fprintf(stderr, "FAIL unexpected check count %u\n", checks); return 1; }
    printf("SUMMARY %u/27\n", checks);
    return 0;
}
