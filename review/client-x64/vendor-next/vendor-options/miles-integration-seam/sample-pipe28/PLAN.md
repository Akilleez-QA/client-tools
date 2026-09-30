# Sample pipe28 prospective source gate

Authored before tests. Work is confined to this new directory; frozen inputs and
the five-function native-sample27 public header remain unchanged. No vendor,
engine, VM, network, playback or callback execution is authorized here.

Inspecting pipe-native26 and pipe-live27 establishes that the existing Session
owns startup, driver and shutdown. Its Channel carries text, not a binary image;
its reply validator does not accept sample allocations or time results. Host27
has a fixed request oracle and no allocation/release owner for these samples.
This gate extends the existing client composition in an isolated staged copy;
it does not introduce another backend selector, lifecycle owner or Hooks table.

Implement four justified public functions: allocate_sample_handle,
sample_ms_position, end_sample and release_sample_handle. Allocate and publish
local proxy storage before the remote allocation request. Retain released proxy
tombstones until Session destruction so addresses are not reused within that
session. A bounded lifetime allocation budget of 64 proxies fails before remote
side effects. The existing Session's sticky fault behavior governs uncertain
exchange outcomes. Validate owned-sample identity and reply shape before writing
any requested signed outputs; preserve null output pointers and their mask.
Reject shutdown while an owned sample is live. Normal confirmed release retires
the local identity; host generation correctness remains a separate dependency.

Named-file binding is intentionally UNIMPLEMENTED, not restricted to one bind.
Its public declaration remains the immutable native-sample27 declaration. The
real Audio.cpp duration helper (4437–4455) allocates a temporary sample, binds,
queries, ends and releases only on bind success. Buffered sound/music paths
(5333–5338 and 5353–5358) reuse an existing sample after stop/end and bind again.
Therefore one-bind-per-allocation would not satisfy the existing native API.
An aggregate bounded, immutable suffix/image preparation primitive may be
implemented; it makes no vendor call and claims no rebind/reclamation policy.

Acceptance, fixed before tests:

1. Apply one explicit overlay patch to a fresh copy of pinned pipe-native26 source.
   Compile/run the real patched Session and decoder with a scripted existing
   Channel. Check null/non-null allocation, owned versus borrowed identity,
   negative time outputs, all four nullability masks, output preservation on bad
   replies, no retry after uncertain allocate/query/release, retirement, stale
   proxy rejection, pre-side-effect budget refusal and shutdown ownership.
2. Exercise the immutable image/suffix primitive with the actual BufferUpload and
   RetainedBuffers implementations: reject unsealed/over-budget inputs and retain
   independent copies. No vendor lifetime is inferred from these tests.
3. Negative link check: use the real five-function sample27 usage object and the
   patched pipe library; linking must fail at the missing named bind function.
   No fake implementation may make that missing component appear complete.
4. Freeze authored inputs before compilation. Retain commands, raw output,
   compiler/input hashes, exit codes and limits. Pure tests use sanitizers; no
   native fixture or real file/SDK callback is run.

Stop on unexpected failures; preserve first evidence. Root receives the scoped
design before tests. No live readiness claim follows even if portable checks pass.

Remaining integration components: actual session binary/sealed-upload path;
host allocation publication and generation retirement; no-callback quiescence
and shutdown ordering; host ownership of image/suffix for successful and failed
bind attempts; documented rebinding behavior; and abnormal-process teardown.
Unknown remote outcomes do not authorize retry, local success, vendor release or
freeing memory still possibly referenced by the vendor. Retention has explicit
budgets and is not offered as an unbounded substitute for replacement semantics.
