# Unexecuted original-context observer patch

`original-context-observer20.patch` is a proposed change to the retained fixture's
`probe.cpp` only. The original file is unchanged. The patch has not been applied,
compiled, or executed. It is diagnostic preparation, not a causal fix or an
authorization to repeat the workload.

It replaces the existing VEH handler's CaptureStackBackTrace with values from
the supplied EXCEPTION_POINTERS::ContextRecord. It prints the interrupted EIP,
ESP, EBP, general registers, context flags, exception address and AV operation /
accessed address. It reads exactly 16 original-stack DWORDs, four DWORDs at the
original ESI, and three at the original EAX through ReadProcessMemory against the
current process. Each of the 23 reads is independent. API failures, partial reads,
and address-arithmetic overflow remain explicit; failed data is never printed as
a valid zero value. No pointer obtained from these words is chased.

The ESI and EAX areas are labelled *candidate* headers. That interpretation only
holds at the free/coalescing instruction independently decoded in
TEARDOWN-INDEPENDENT20.md. For any other AV they are merely register-addressed
memory. The handler makes no assertion about ownership, block validity, or which
return address belongs to which function.

## Artifact-specific interpretation

In the **old retained probe.exe**, at EIP `00421494`, let S be original ESP:

* `[S+8]` is free's return, `[S+12]` userPointer, `[S+16]` array argument.
* If `[S+8]` is scalar-delete return `00420e80` or array-delete return
  `00420ec0`, `[S+20]` is the owning delete return site.
* Owning return `0041a13d` identifies ExitChain entry deletion; callback ancestry
  can instead include the indirect-callback return `0041a12e`.
* Original ESI is userPointer minus 16, and original EAX is its previous-block
  pointer at that instruction.

**Those addresses belong to the old executable.** Building a changed observer
can move code and change optimization/link selection. Before interpreting a new
capture, retain its exact executable/map and disassemble its free prologue,
delete wrappers, and ExitChain call sites again. Even the stack offsets above
must be revalidated against that artifact. The patch therefore prints raw words
and does not embed old addresses or automatically label stack words as returns.

## Behavioral limits

Playback, bootstrap, cleanup ordering, callback ownership, and all vendor and
allocator calls in the fixture remain untouched. The handler always returns
EXCEPTION_CONTINUE_SEARCH. A diagnostic-only interlocked guard bounds reentry:
a nested or simultaneous invocation skips observation and continues normal
exception dispatch; it does not swallow the exception or resume execution.

The observer retains the fixture's existing printf transport. printf is not
guaranteed to succeed in a damaged process, and these observations are not a
substitute for a full original-context crash dump. Memory reads are bounded and
guarded, but capture is not an atomic memory snapshot: other threads may change
memory. At the decoded fault the allocator has already set the free bit and
updated counters, so this observer cannot reconstruct pre-free validity or the
allocation's historical owner.

Review/validation performed here is source reasoning only. No execution or
compilation was performed, and no claim of a repaired baseline is made.
