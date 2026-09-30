#include "test_allocators.h"
#include <cstdlib>
#include <new>
bool denyAllocation=false;
MilesFileOwner36::SessionFileOwner *failAfterReservationOwner=0;
bool reservationFailureTriggered=false;
void *operator new(std::size_t n){if(denyAllocation)throw std::bad_alloc();
    if(failAfterReservationOwner){
        MilesFileOwner36::SessionFileOwner::FileState state;
        MilesWire::Handle h={MilesWire::File,1,1};
        if(failAfterReservationOwner->fileState(h,state) && state==MilesFileOwner36::SessionFileOwner::Reserved && !failAfterReservationOwner->retainedOperations()){
            reservationFailureTriggered=true;throw std::bad_alloc();
        }
    }
    void *p=std::malloc(n?n:1);if(!p)throw std::bad_alloc();return p;}
void operator delete(void *p) noexcept {std::free(p);}
void *operator new[](std::size_t n){return ::operator new(n);}
void operator delete[](void *p) noexcept {::operator delete(p);}
