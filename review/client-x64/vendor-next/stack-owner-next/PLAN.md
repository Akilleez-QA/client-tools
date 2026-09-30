# Ordinary stack ordering diagnostic

Only named noinline function chains call actual production DebugHelp::getCallStack. Capture _ReturnAddress directly at leaf/middle/outer sites; print raw addresses and exact stack-slot matches. Post-call volatile side effects preserve ordinary call frames. A separate tail-eligible noinline middle records whether optimization removes its frame. No allocator calls, invalid allocations, null frees, owner setters, deliberate faults or modified MemoryManager policy are exercised; genuine supporting core initialization only.

Prediction: retained-frame return addresses appear in ascending stack indices. Win32/x64 first-slot conventions may differ; record rather than force agreement. Tail-eligible frames may disappear in Release, so fixed owner offsets cannot be inferred from frame count alone. Optional MemoryManager allocation uses OFFSET3 for owners1+, setOwner OFFSET2 for owners0+; observed ordinary ordering alone is not allocator ownership validation.

Build genuine DebugHelp.cpp with real headers and previously verified core libraries, both ABI/configuration combinations in unique private directory. Preserve code hashes, command lines and raw output. Source/linked dependencies are diagnostic snapshot, not the ongoing product build. No active VM mappings or source edits.
