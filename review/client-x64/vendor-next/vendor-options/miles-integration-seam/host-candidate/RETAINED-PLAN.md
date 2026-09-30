# Retained buffer experiment contract

Declared before native execution: pure ownership only; no vendor SDK dependency or calls. Per-resource stores stage immutable copies under explicit entry/byte caps, commit without freeing old/staged content, retire only by caller action, refuse active retirement. Both successful and failed vendor bindings require separately proven reference termination before releasing any possibly retained data. Destructor/deactivate are caller quiescence preconditions, not vendor synchronization.

Process-unique monotonic atomic tokens prevent accidentally accepting another store's token. They are internal IDs, not pointer values or wire authority. Store operations remain dispatch-thread-owned. Exhaustion rejects further staging; allocation exceptions propagate without changing active/token accounting.

Native v120 x86/x64 Debug/Release /W4 /WX; ordinary small buffers and exact null/empty C strings, binary zeros, boundary spans, cap rejection, old pointer persistence, cross-store isolation. Linux ASan/UBSan plus three safe mutants: allow active retirement, erase prior copy at commit, omit byte cap. No actual oversized resources or destruction while vendor retains data are executed.
