# Step31 successor: checked join and scoped object gate

Source-only successor to frozen file-executor30. The private namespace/type names are deliberately unchanged to keep the correction narrow. `checked-join-from30.patch` contains the entire mechanism change: a protected-handle checked wait in the owned Thread subclass, plus corrected failure contracts. FileInvocationJob sources are byte-identical to step30.

`Thread::wait()` discards the OS wait result. Step31 instead accepts only WAIT_OBJECT_0. Any other result returns false from drainAndJoin with the thread pointer and owner reference retained; it performs no subsequent dereference or resource destruction and never claims TLS teardown completed. Intake remains closed. The owner must retain the worker and dependent engine resources; this code does not retry, force-terminate or destroy them. Engine Thread itself is unchanged.

`create()` returns NULL for a caught allocation exception; that is not a universal recovery guarantee. Actual engine MemoryManager allocation can FATAL. Thread creation failure still releases the owner and unused initial self reference only when _beginthreadex returned a null handle. A successful thread is owned through its checked join, including Thread::threadFunc TLS removal.

All other step30 scope and integration limits remain: engine-owned FIFO; opaque pointer/function boundary; separately compiled modern file26 adapter; no direct modern-STL/engine-STL layout sharing or cross-boundary deletion; independent receive progress; existing coordinator/pin policy remains external. Global-file/FileOpen admission mapping, vendor termination evidence, residual-close adapter, actual Audio partial-install ownership and fatal teardown remain unresolved. The prototype is not connected to product execution.

The proposed gate is **20 object compilations**, five TUs × Debug/Release × Win32/x64. No baseline step30 compilation is needed to discriminate this new source's type/include compatibility, and no full-Audio recompilation is included. The frozen step29 matrix already covers the common-body seam; it does not prove this worker compiles or links. This gate deliberately does not link or execute any engine code.

`prepare-native.py` prepares only a fresh local input directory, verifying the pinned49d0 checkout, previous step29 snapshot, and frozen30 manifest first. `run-native.py` is the exact proposed VM-side driver, not executed during source preparation. It stops on the first failed compile, COFF machine or STL include-boundary check; there is no retry path.
