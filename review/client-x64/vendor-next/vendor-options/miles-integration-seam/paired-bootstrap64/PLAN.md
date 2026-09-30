# Paired bootstrap64 — source-only return-order correction

Preserves59 unchanged. No compilation, tests, VM, SDK/engine runtime or product edits. This remains an incomplete private bootstrap;61 public-boundary composition, callback TLS adaptation, locks and normal teardown are not added.

## Concrete ordering correction

The private Channel call now receives a const reference to its existing Session reply owner. After the same exact wire/installation decoder and **before** Runtime::returned, LiveChannel calls `Session::validateReply(opcode, originalFields, decodedReply)`. No new registry, transport field, public argument, ownership type or effectful callback was introduced.

The pure owner validation checks successful pairs against the exact requested output mask: legal topology, zero bits for omitted outputs, equality for aliased output pointers. It covers sample/stream millisecond pairs and sample volume/reverb pairs. Speaker output respects the existing single selected output. Stream alias success must echo the exact requested parent; that parent must be live in the existing stream list. A previously published alias cannot become null or change identity, and another parent cannot already own that exact alias. New stream/sample allocation identities cannot duplicate existing live rows; driver success cannot replace an existing driver. Generic decoding still enforces allowed fields/status/kind/extent. No generic decoder was weakened.

Known, fully wire-validated refusals pass this extra success-only validation and still run returned/join before Session::request propagates checkStatus. A malformed request-dependent or owner-dependent success fails in LiveChannel's existing catch, requests Runtime failure, and reaches Session's faulted catch without posting returned. Its published admission/resource pins therefore remain retained. The validator itself does not mark failure, mutate proxies, write caller outputs, enqueue work, allocate another registry or settle admissions.

Duplicate stream/alias/pair checks formerly after the join were removed from public operation bodies. Their subsequent result publication and scalar/output writes remain after Session::request returns. Pre-request allocations of unpublished proxy storage remain intentionally unchanged: those reservations precede native effects and are retained on uncertainty. No wire result is published to those reservations before the join.

## Other requested corrections

- `host_sdk_callbacks.cpp` is byte-identical to host-runtime58's setter-only correction: remove the known v120 /EHsc-unreachable catch around extern-C setter, retain all actual callback thunk catches.
- Session destructor contains only the temporary terminal invariant guard, with no unreachable old cleanup. Session/Channel comments now state normal close is unavailable. This does not select final shutdown behavior or add cleanup.

## Bounded portable test proposal — NOT authored or executed

First freeze/review any test-only dependency substitution separately. Use actual64 Session reply validator and existing real result/protocol types with selected proxy rows; isolate only the private Runtime/Channel dependencies needed to construct the owner. No Windows Endpoint, real EngineFileWorker, engine allocator, DLL or process-fatal destructor may execute. A scripted return-observation sink and coordinator fixture must be labeled portable, never real Runtime evidence.

Discriminating cases:

1. Valid zero/null pair fields and masks0/1/2/3/7; omitted-output nonzero and unequal alias-output bits for all four pair opcodes. On rejection: zero returned-observer calls, admission/resource pins retained, no caller outputs changed.
2. Wrong stream-parent echo, missing live parent, null after published alias, changed published alias and identity already owned by another stream. Accept initial null, initial valid alias and stable repeated alias. Reject before return observation and preserve the original proxy rows exactly.
3. Duplicate live stream/sample allocation identities versus legitimate null/new identity. Preallocated nonlive rows must not be mistaken for duplicates or be published before join.
4. Known validated refusal: record return once before refusal propagation; no alias/pair-success interpretation. Malformed generic frame or install echo: no owner validation completion and no returned observation.
5. Valid success with pending causal callback: validation first, returned observation next, join remains pending until actual scripted ACK, then publish output/proxy. Rejected result must not gain permission to acknowledge or release that admission.

A portable supplier cannot by itself prove actual LiveChannel call order. Keep the source oracle explicit: in actual exchange, generic/dedicated decode precedes `replyOwner->validateReply`, which precedes `runtime_->returned`; failure catch calls fail. A later native compile gate verifies this real TU separately. Do not test only a rewritten sequence or claim whole Win32/runtime behavior from a scripted channel.

## Provenance

All candidate files copied from59 except four private client files changed here and the single58 SDK setter file. `candidate.patch` is the complete diff against59; `provenance.json` records origins and hashes; manifests freeze production sources and this plan. No tests/build runner are supplied. The parent review is the next gate.
