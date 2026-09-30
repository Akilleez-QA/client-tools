# Crypto Debug x64 packing diagnostic

Observation: frozen matrix crypto FirstCrypto.cpp fails /WX at STLport
stl/_prolog.h:16, C4103. STLport config/_prolog.h deliberately pushes pack8 and
config/_epilog.h pops it. Nested include boundaries therefore differ from native
x64 pack16 even when the complete include restores the incoming state.

Native v120 layout probe, actual FirstCrypto.h, real matching STLport library,
Debug/Release on both ABIs: all four builds/runs succeed with /W3 (no /WX in this
diagnostic). x64 pack(show) is16 both before/after, Win32 remains8. Struct carrying
an explicitly aligned SIMD member stays size32/member offset16 before/after.
std::string is12 on Win32/24 on x64, BufferedTransformation4/8. This is bounded
layout/state evidence, not exhaustive crypto ABI correctness or cryptographic tests.
V1 probe linked unsuccessfully because the autolink library search path was absent;
v2 names the real matching archive and disables only the redundant autolink name.

Proposed smallest fix, pending parent approval: within FirstCrypto.h only, guard
_MSVC/_WIN64 warning(push), warning(disable:4103), the existing three vendor includes,
then warning(pop). Keep every packing pragma unchanged and preserve /WX globally.
Verify original warnings reproduce, fixed entire crypto project builds all4, same
layout probe, and deliberate later unbalanced-header negative control still fails
with C4103. This distinguishes scoped treatment from blanket warning suppression.

Reject /Zp8 for the entire project: changes unrelated structure ABI and SDK layout.
Reject global /wd4103 or disabling /WX: hides actual future packing regressions.
Reject STLport pack16 rewrite: changes library layout and broadens scope.

Primary documentation:
- https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/compiler-warning-level-1-c4103
- https://learn.microsoft.com/en-us/cpp/preprocessor/pack
- https://learn.microsoft.com/en-us/cpp/build/reference/zp-struct-member-alignment
Microsoft documents default native x64 pack16 and explicitly warns against
changing packing while including Windows SDK declarations. The balanced observed
state supports a narrow diagnostic exception, not changing the ABI.

## Version binding and expanded roots

PCH-only v1/v2 leave later count warnings; all failed native logs retained.
The complete v2 build (four files) passes all four configurations, but its header
still preloads deque/memory unconditionally. Parent requested these includes be
x64-only, so the final header is being rebuilt as complete v3 before claiming
current-candidate acceptance. Production packing remains unchanged.

Separate count roots now implemented for review: StringStore checks both implicit
size_t lengths against UINT_MAX using this old library's existing Exception;
MessageQueue prevents adding a completed message beyond UINT_MAX before mutating
its always-nonempty deque, then casts its count under that invariant. AnyMessages
spells the existing boolean conversion as !=0. No modern Crypto++ API assumed.
Real small-input/synthetic-limit-constructor runtime tests pass Win32 both modes
and x64 Release; x64 Debug test link waits for actual fresh core archives from the
ongoing immutable matrix. No huge input transfer or huge queue proof implied.

## Final candidate evidence

Complete v3 source hashes (four files) match local candidate exactly; manifest is
crypto-candidate-manifest.json. Actual crypto project builds all4 with original
warning policy. Final positive header /WX controls pass4/4; deliberate unbalanced
header after it still fails C4103 in all4. Final before/after layout probes match
original values in all4; no packing-setting change.

Runtime checks: Win32 Release/Debug10/10, x64 Release/Debug12/12. Actual StringSource
C-string/generic-view/raw bytes transfer unchanged; synthetic UINT_MAX view is
constructed but never transferred; UINT_MAX+1 rejects with exact old-library
Exception on x64. Real small queues exercise completion count, swap and retrieval.
Huge-queue boundary is arithmetic only; no allocation of billions of deque entries.
Debug-x64 v3 link failed on an unused missing network-message archive; v4 records
and omits nonexistent optional core archives, resolves against real current MM
and STLport, and passes12/12. No substitute operator or allocator supplied.

Independent sibling source critic confirms nonempty queue/count invariant and
constructor rejection; this is source review, not independent native reproduction.
Existing cumulative message-byte unsigned-long overflow in Put is unmodified and
not covered by the new completed-message count bound. Only the Windows-guarded
FirstCrypto wrapper change is mirrored to server-client-compat; no old Crypto++
algorithm/count changes backported into the upgraded server vendor dependency.

Discrimination: unchanged runtime fixture compiled with original94a filters.h
returns exit4 at the oversized template-view constructor instead of rejecting;
candidate returns0. Control compiles successfully, so it discriminates runtime
narrowing behavior rather than merely missing API/build differences. Evidence
C:/crypto-unchecked-control-v1; synthetic view remains untransferred.
