# Sample pipe28 — partial source composition

The new candidate implements four of native-sample27's five sample functions in
an isolated overlay of the existing pipe-native26 client composition. It does
not implement named binding and is not usable as a complete live sample backend.
Frozen inputs and the original five-function public header were not edited.

## Observed portable results

First run of `python sample-pipe28/check.py`:

| Check | Exit | Observed result |
|---|---:|---|
| Apply overlay to pinned source | 0 | Real Session/client/decoder staged |
| g++ C++11, warnings as errors, ASan/UBSan build | 0 | Portable test linked |
| Scripted existing-Channel test | 0 | 379 assertions |
| Link actual complete duration helper | 1 | Expected missing `ClientMiles::set_named_sample_file` |

The negative link log contains that unresolved binder and no other unresolved
facade operation. No binder stub was supplied. The test uses encoded responses
and the actual modified typed reply decoder, not direct fake function returns.
Tests remain scripted and are not vendor or engine runtime evidence.

Coverage includes proxy-allocation failure before a remote call; nullable remote
allocation; all four millisecond masks and negative values; unchanged outputs on
refusal/bad results; borrowed-sample rejection; terminal uncertainty after
allocate/query/release; release retirement and retained local tombstones;
pre-call budget refusal; and shutdown refusal with live samples. PreparedInput
uses the actual BufferUpload/RetainedBuffers helpers to check sealed input,
aggregate budget and independently owned suffix/image copies.

All inputs in the pretest receipt were unchanged afterward. Source manifest was
frozen before tests; no repair or repeat was needed. Commands, raw logs, the
compiler identity, staged sources and exits are in `evidence-v1/`.

## Identity

- Authored source manifest: `3c824e817041d4f1c5dc6742c9b637144658faf72a93aebd1f7d67648f96e80e`.
- Authored source archive: `a3df5c01180785546252a8aef8128f81395753974f1f9130adccee984a216331`.
- Pretest receipt: `c0139e6780ffa7af872dfbd45f786b71c916e605aa96155d35e35eed8d4dd5b1`.
- Final receipt: `79aade498846ba4824958fb106b960f2732a10dab9419a1dacd931456d1da2ab`.

`FREEZE-v1.json` records these identities. The source archive contains this
candidate's frozen authored inputs; external frozen dependencies are named and
hashed in the input/pretest manifests. The checker currently uses those local
workspace paths and requires a fresh evidence-v1 output directory.

## Exact implementation gap

There is no host sample allocation/publication/release owner, generation
retirement proof, binary upload connection or bind adapter. Existing generic
host query/end code does not supply those missing pieces. Host27's fixed oracle
and real process composition are untouched. Neither a live process nor vendor
library was launched. The next integration step must implement the shared
Backend/registry sample owner and validate these four operations there before
claiming an end-to-end path.

Named binding/rebinding needs actual vendor retention/replacement semantics for
both image and suffix after success and failure. PreparedInput only prepares
stable bytes; it does not solve that ownership transaction. The reused buffered
sound/music call sites remain documented in DESIGN.md. There is no one-bind
policy and no unbounded keep-every-buffer workaround.

The 64-tombstone budget and pointer lifetime are explicit prototype boundaries.
The existing error enum still reports remote InvalidResource as InvalidDriver.
Also, source argument order is not proof of vendor aliasing behavior: the client
query writes total then current after acceptance, but fidelity when both output
pointers alias has not been established against the SDK. No intermediate output
write or exceptional vendor behavior is reproduced by a successful scalar reply.

Plan and scope were handed to root before testing. No VM, SDK link/native run,
product/frozen-file edit, PR, push, new CLI review or playback was performed.
