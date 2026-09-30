# Buffer upload source review

2026-09-30. Independent bounded review of `vendor-options/miles-integration-seam/buffer-upload-candidate/{PLAN.md,buffer_upload.h,buffer_upload.cpp,tests.cpp}` and the existing codec/RetainedBuffers interfaces. No execution, product edits, or new agents. The reported 29 sanitizer checks were not rerun or treated as correctness proof; native verification was pending in the task framing.

**Result: no concrete bounds, exception-publication, immutability or ownership defect found in this source snapshot.** The class supplies sequential assembly and independent publication. It can complement the codec and RetainedBuffers safely when the caller supplies their stated preconditions. It does not implement wire handlers, resource authority, aggregate budgets, vendor binding or retirement.

## Observed properties and their limits

**Bounds — no defect found.** `buffer_upload.cpp:5–8` rejects declarations beyond the authorized limit before allocating. The class invariant is `0 <= filled <= storage.size() <= UINT32_MAX`. Initially filled is zero; append (`10–14`) requires the exact current prefix and checks `count <= storage.size()-filled` before writing. Consequently the subtraction cannot underflow, conversion of an accepted count to uint32 cannot truncate, and the final addition cannot wrap. A nonzero accepted count also guarantees that `&storage[filled]` names an element, including when the buffer was initially empty. Invalid offsets/gaps/overlaps/replays cannot change the prefix. These are source deductions, not a measured maximum-size allocation claim.

**Source pointer — explicit caller prerequisite.** `append` rejects null and zero length but cannot establish that a non-null pointer actually covers `count` readable bytes. That is normal for this internal copying API. The coordinator must derive pointer/count from a successfully decoded, still-live frame, not pass a received offset as an address. `codec.cpp:135–155` checks total frame size and canonical spans; `75–102` supplies frame and subtraction bounds. No internal upload pointer is exposed, so ordinary supported use cannot alias the private destination storage. This is not a finding against BufferUpload; calling it before source-span validation would be a caller defect.

**Immutability/coverage — no defect found.** Seal (`16–19`) succeeds only when the received prefix equals the declaration. Sealing an empty declaration is structurally consistent. Repeat seal is idempotent. After sealing, every append rejects before mutation. There is no setter or mutable view through the public interface (`buffer_upload.h:9–23`); copying/assignment of the object itself is disabled. The stated dispatch-thread ownership remains necessary: these fields are not synchronized for concurrent readers/writers.

**Exception publication — no defect found.** Constructor allocation failure means no complete object is published. Append does not allocate. `copySealed` first creates a local vector copy and only then swaps with the caller output (`21–25`). If construction of that copy throws, the sealed upload and preexisting output are unchanged; if unsealed, it returns false before touching output. The default-allocator vector swap transfers ownership. This method can throw even though its return type is bool: the caller must handle allocation exceptions and restore any reserved budget without reporting a successful Buffer publication. The plan correctly describes this boundary. I did not inject allocation failures.

**Ownership — no defect found.** The returned vector has its own allocation; replacing or destroying it does not mutate the upload. Destroying the upload cannot invalidate that vector. `tests.cpp:25–32,39–42` meaningfully checks source mutation, destination mutation, repeated publication and upload destruction. No vendor pointer escapes from this class. The source confirms the intended claim, independently of the reported check count.

## Composition with RetainedBuffers and the codec

The safe sequence is: assemble and seal the session-owned Buffer; copy into a temporary owned vector; stage its complete bytes into the sample's RetainedBuffers; resolve the staged local view for the real SDK bind; retain that sample-owned copy until the established vendor retirement boundary. `retained_buffers.cpp:18–38` copies input during staging. After successful staging, destruction of the publication vector and upload cannot invalidate the retained entry. A failed bind does not itself authorize retirement of staged bytes.

Empty uploads may seal, but RetainedBuffers deliberately rejects empty Binary input (`retained_buffers.cpp:24–26`), and sealing says nothing about a valid WAV or other vendor format. The coordinator must preserve that distinction rather than bypass the retained-store check. A complete arbitrary byte string is not parser-validation evidence.

There is no 1 MiB **asset** restriction in BufferUpload. The declaration remains uint32 and subject to its authorized per-upload bound and available allocation capacity; “unlimited assets” would be false. `tests.cpp:43–51` assembles `MaxFrameBytes+17` through chunks sized to fit a 136-byte call envelope. This proves the intended assembly example at source/test-design level. It does not actually encode/decode those chunks or exercise a BufferChunk handler. `codec.cpp:78–86` separately bounds the whole frame; the future handler must apply that codec before append and must enforce the Buffer operation's allowed fields.

Aggregate budgeting is **not implemented here**, as `PLAN.md:5–7` and `buffer_upload.h:7` state. Budgeting must account for storage allocated upfront, repeated `copySealed` calls and their replacement-output overlap, and further RetainedBuffers staging copies. Peak payload storage can exceed merely “upload plus one published copy” during staging; standard-library temporary/capacity overhead adds more. An authorized limit is a per-upload declaration check, not an exact RSS guarantee. This is a documented integration obligation, not an invented component bug or reason to add another ownership graph to this class.

## Verification assessment and next useful check

The test source covers the advertised sequential-state rejection cases, ownership separation, empty behavior and larger-than-frame assembly. It does not establish native v120 compatibility, allocation-failure observations, session authorization, aggregate-budget enforcement or the actual upload-to-retained-store handoff. No such results should be inferred from its 29 checks.

When the real handler is authored, the useful composition check is a multi-frame upload through the actual codec into this class, publication into RetainedBuffers, destruction of upload/publication storage, then validation of the retained bytes before a genuine bind. Include rejection of premature publication and append after seal, preserving an already retained image on failure. This recommendation is prospective; no workload was executed here. No unrelated RegistryResolver C4512 declaration change was treated as evidence about runtime behavior.

## Exact reviewed identities

Paths are relative to `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam`.

| File | SHA-256 |
|---|---|
| `buffer-upload-candidate/PLAN.md` | `6ad4037c35540832de4d2d53dee3a8d49716392057db0ed9cfbda85149f23237` |
| `buffer-upload-candidate/buffer_upload.h` | `a3fef35e517a2f3a8d6bc96592f09876eca61ae8241686059160ca1a751d889e` |
| `buffer-upload-candidate/buffer_upload.cpp` | `e36e074e1031f4df9366b865131e7575045a0d497c07219b576f3ce419fd9bd5` |
| `buffer-upload-candidate/tests.cpp` | `53c46ff9def13882c13ce7283ad8cf5773da15d32b046caa6cd35233da1304f6` |
| `host-candidate/retained_buffers.h` | `e62c472f1e46f783a130da8081bb92e958d8e3acaa9010d2fabae6169f329d8e` |
| `host-candidate/retained_buffers.cpp` | `9f8fc1f78238b0347e25606fdc1be658414b73aefb021c3ef91577bcd45d7401` |
| `transport-candidate/codec.cpp` | `15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e` |
| `protocol-candidate/miles_wire.h` | `8efe3915744250a6aebdc51caa712790f4930c2b32877e9425dcf79c191df0b9` |
