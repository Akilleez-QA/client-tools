# x64 DebugHelp stack-failure critic

Read-only source review plus primary Microsoft documentation. Parent reports v3
Win32 257/257, while x64 returns current DebugHelp then a bogus kernel frame and
misses the known caller. This report has not independently executed the VM probe.
Do not call the capture implementation correct based on compile success.

## Header/ABI assessment

Vendored STACKFRAME64 has the same fields/order as the current documented API.
Vendored KDHELP64 ends in Reserved[5] (40 bytes); modern definitions replace that
with two DWORDs, one DWORD64, two DWORDs, Reserved0[2], also40 bytes. No clear size
mismatch follows from this header age alone. Under ordinary x64 alignment expected
ADDRESS64=16, KDHELP64=112, STACKFRAME64=264. Confirm native sizeof/offsetof from
both separately compiled SDK and vendor headers, with exact project flags and
/showIncludes. Context must be the native aligned AMD64 CONTEXT (not a copied
32-bit surrogate). The current code uses native CONTEXT/RtlCaptureContext.

Microsoft documents x64 AddrFrame as RBP or RDI, sometimes unused. Current RBP is
not evidence of a bug. Changing it to RSP before discriminating callbacks obscures
root cause. StackWalk64 API function-pointer argument widths match source.

## Highest-value diagnostic

Run same known noinline chain and captured context in four diagnostic modes:
1. direct SymFunctionTableAccess64 + direct SymGetModuleBase64;
2. cached function table + direct module base;
3. direct function table + cached module base;
4. both original caches.
Record every raw PC/SP/frame before/after StackWalk64, its BOOL, immediate error,
module base, function-table pointer and copied three DWORD runtime-entry words.
Log loaded dbghelp full path/version and module load base/machine. Do not rely on
symbolization to establish frame addresses: compare captured raw values to known
caller ranges/disassembly, and record Return/Stack addresses as well.

The custom function-table cache retains PVOID from SymFunctionTableAccess64 across
other DbgHelp calls and future walks. Documentation identifies x64 result as
_IMAGE_RUNTIME_FUNCTION_ENTRY but supplies no persistent-pointer lifetime promise.
A borrowed/reused buffer is a plausible cause, not confirmed. Logging copies before
and after next lookup discriminates it. Compare to native RtlLookupFunctionEntry
results for the same PC/base. A fresh process first-walk failure alone would not
clear the cache: multiple lookups can happen during that first walk.

All getCallStack work is inside the same scoped critical section, including cache
callbacks. install/remove lifecycle remains quiescence-only, but absent concurrent
teardown it does not explain this deterministic first-chain failure. Cache entries
are keyed by full DWORD64; source no longer truncates dwAddr. Module-base cache
values are also DWORD64. Existing caches can be stale across unload/reload; the
fixed executable probe should distinguish this from startup capture failure.

If direct callbacks fix the failure, remove/bypass only the proven bad cache on
x64 first (or own the returned record only after validating its contract), retaining
Win32 behavior. If direct callbacks fail, compare minimal SDK-header direct
StackWalk64 against RtlCaptureStackBackTrace/RtlVirtualUnwind on the same actual
chain; investigate capture/headers/module registration before replacing APIs.

## Primary sources

- https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/ns-dbghelp-stackframe64
- https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/ns-dbghelp-kdhelp64
- https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/nf-dbghelp-symfunctiontableaccess64

No production or VM changes made by this critic.
