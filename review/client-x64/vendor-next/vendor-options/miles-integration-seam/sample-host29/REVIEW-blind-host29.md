# Independent source review: sample-host29

Reviewed 2026-09-30. **Source verdict: no blocking correctness defect found in the intended four-operation Backend overlay under its single-dispatch-thread, no-callback-registration contract.** It supplies the allocation/release lifecycle and query/end routing missing from sample-pipe29's Backend. **Integration verdict: incomplete.** The frozen prepared package remains a host-source overlay over the old live27 fixture, not a composed working sample client/host. Named-file binding remains absent.

## Scope and independence

Read both raw patches and actual prepared Backend/registry first. Inspected the call routing, SDK dispatch source, common `require` helper, prepared host entry point, admission logic, reply decoder, preparation script and frozen manifest. Did not read author results, receipts, test logs, existing reviews, or authored test code. The earlier independently reviewed sample-pipe29 client remains a separate artifact; its behavior was not assumed present in this prepared tree.

No frozen source edits. Added only this report and `review-scratch-host29/`. No vendor, native SDK, Backend stub, real host, VM, engine, game or audio runtime execution. No descendant agents. The independent portable test plan was written before its test.

## Four-operation source assessment

### Allocation and exception ownership

`prepared/startup-bridge23/backend.h:72–105` validates shape and running state, resolves a Driver before allocation, then reserves an OwnedSample slot before invoking `AIL_allocate_sample_handle`. `ResourceRegistry::reserve` allocates only while extending its vector; its remaining updates are scalar writes. If reserve throws or returns false, no vendor allocation has happened. Capacity failure is terminal through `require`, rather than being misreported as a vendor-null allocation; that is conservative but honest.

`PendingSample` is constructed before the vendor call. Once the native call returns a nonnull pointer, the guard owns it until nonallocating `publish` commits the registry identity. Failed publication throws with the guard still armed and therefore releases the unpublished sample during unwinding. `require(bool,const char*)` performs no allocation on its successful path. After publish succeeds, clearing the guard is a nonthrowing pointer assignment. A later reply-encoding/transport failure leaves the sample in host registry tracking and results in Backend shutdown on unwind; it must not be interpreted as an observed release by the client.

A vendor-null return leaves the output resource zero and cancels the unexposed reservation at scope exit. It is not conflated with failed reservation or invalid target. Driver opening now similarly reserves before the native open. Unlike PendingSample it relies on the existing started Backend destructor calling vendor shutdown if publication fails; the host entry point does unwind that Backend on an escaping C++ exception. These guarantees cover ordinary C++ failure paths, not process termination or vendor faults that do not return/unwind.

### Identity, parent and generation

`prepared/transport-candidate/resource_registry.h:88–134,163–180,190–215` stores reservation identity by slot/generation rather than retaining vector-element pointers, so vector growth does not invalidate the token. Tokens are noncopyable and registry-bound. State 4 is invisible to resolution, close and ordinary retirement. Publish verifies registry ownership, kind, generation and reservation state; its failure preserves caller output. Cancellation clears an unpublished reservation without consuming a generation, which is appropriate because it exposed no wire identity.

Every OwnedSample created by the new Backend path records its actual Driver handle as parent. Resolution requires that exact parent generation to remain live. Successful retirement increments the sample generation or permanently exhausts the slot at the configured limit. Driver retirement walks its matching children without allocating and retires them before the Driver entry. Retirement of another Driver leaves the sample alone.

The existing public `insert(OwnedSample,...)` can still create unparented legacy entries. That is not introduced by this overlay, and the new Backend allocation path does not use it. Do not extend the overlay's parent guarantees to arbitrary external registry users. Likewise, tokens must not outlive their registry or be published across parent closing; the Backend's stack-local reservation and serial execution meet that documented contract. No broader concurrent/reentrant lifetime guarantee is claimed.

### Release, repeat use, query/end and shutdown

The new release route resolves only a live OwnedSample, calls the real `AIL_release_sample_handle`, then retires its identity. Under the serial/no-callback contract no intervening registry mutation occurs, and `retire` does not allocate. Invalid/stale/wrong-kind targets are refused before the vendor call. Repeated ordinary allocation/release reuses free slots with changed generations rather than accumulating tombstones.

Query/end are now explicitly forwarded at `backend.h:49–50` to the existing SDK dispatcher. The dispatcher's query case preserves the two nullable S32 outputs through a mask and bit encoding; end does not retire an allocation. These routes require a running Backend and use the registry resolver, which now checks the sample's parent.

Shutdown ordering at `backend.h:193–203` is vendor shutdown first, then local driver/child registry retirement, then successful reply. This avoids deleting tracking before the vendor has returned from shutdown. The emergency destructor calls vendor shutdown while members still exist and logs failure cleanup; it does not manufacture successful protocol cleanup. The registry is bookkeeping, not an owner that invokes vendor functions on its own. Actual Miles shutdown completion/quiescence remains native evidence to obtain, not a fact established by a portable registry test.

## Remaining integration gaps

### P1 integration gate — Frozen prepared package is not composed with the sample client or a sample-capable entry point

`prepared/pipe-live27/host.cpp:38,55–56,97–100,115` still instantiates Oracle27 and rejects requests that do not match its fixed 22-opcode sequence. The new Backend's arbitrary ordinary sample operations cannot be exercised through that entry point as supplied. This is inherited fixture behavior, not a regression in reservation logic.

`prepared/startup-bridge23/reply.h:76–83` still permits resources only for digital-driver open and has no sample-time result allowance. A successful nonnull allocation or nonzero sample query would be rejected by this packaged client's decoder. The packaged ClientMilesPipe.cpp also has no allocated-sample implementation. The separately reviewed sample-pipe29 client patch supplies those pieces, but this preparation script does not apply it.

Therefore accept this artifact as a Backend/registry overlay only. A separately frozen composition needs the repaired client/decoder and an appropriate host entry point before claiming even four-operation end-to-end readiness. This report does not require broadening the overlay into a general audio engine.

### P1 full-sample integration gate — Named-file binding and retained input lifetime remain absent

Neither patch adds `set_named_sample_file`, upload ownership, failed-bind/rebind semantics or host retirement of its image/suffix storage. This overlay does not hide a binder behind allocation. It closes the narrow host lifecycle omission, while the earlier missing-binding finding still stands for the intended duration/file workflow. Merely allocating/querying an unbound sample cannot establish that useful workflow.

Native VS2013 x64 client / x86 original-DLL compilation/linking and real transport/vendor behavior also remain unverified by this review. No native SDK64 binary is assumed or required as a substitute.

## Independent checks

Wrote a bounded portable test against the actual prepared registry header, built with GCC 16.2.1 and `-std=c++11 -Wall -Wextra -pedantic`. Compilation produced no diagnostics; execution exited 0:

```
PASS bounded actual-header registry checks; no vendor/host/native execution
```

Coverage: hidden reservation state; null/foreign-registry publication rejection and unchanged output; cancellation without generation burn; 64 successful publication/retirement cycles reusing one slot; stale-generation rejection; separate Driver isolation; parent-close refusal and parent-retirement invalidation; finite generation exhaustion without wrap/reuse. Native allocation/release/shutdown ordering was examined in source only. No allocator fault injection or mock vendor API was used.

Independently verified all 39 manifest entries against both the prepared files and frozen archive member contents. Both authored overlay headers exactly match their prepared counterparts. These checks establish source identity, not correctness of uninspected files or runtime approval.

Reproduction from this artifact directory:

```
c++ -std=c++11 -Wall -Wextra -pedantic -I prepared review-scratch-host29/registry_blind.cpp -o review-scratch-host29/registry_blind
review-scratch-host29/registry_blind
```

## Exact identities

Paths below are relative to this report. The manifest/archive identities bind the frozen input; the explicit code hashes identify inspected implementation surfaces. A machine-readable copy is in `review-scratch-host29/source-hashes.json`.

- `patches/01-resource_registry.patch`: `e19f39b81fd9f355c7f6b5c2e2e70a0e2fdcbea3d919865967cbb145d2fa8c04`
- `patches/02-backend.patch`: `f2366fb9638e3ad82b56d3b6a92fdfd8de582b50010eac38229d579aba04cf6b`
- `source-manifest.json`: `70d84b2f848bbcc234fc0f7c69dd5f80f0e72effee614d160b539e7623c0a836`
- `source-v1.tar`: `050fa0df52f6a81f529aa701307219c25a801bfd0133cc655b853a740fedbffc`
- `prepare.py`: `d67ffa4742afc2200be1c8b1086d8800d74a4462d83702ee5f9d3c3f0969fb51`
- `prepared/startup-bridge23/backend.h`: `b2dcd7e56cf539fe96a09155dcd0815e0077b47c9c2e91dfd882e22bd153650b`
- `prepared/transport-candidate/resource_registry.h`: `148903889b0bd498f394dc05f3b50738e4924068d245430dfadb74544276509b`
- `prepared/startup-bridge23/reply.h`: `99bbe94d1ae635d9040b751da1dbd077df82d4e8ff2027b016c85c7ee36560e5`
- `prepared/host-candidate/host_dispatch.cpp`: `4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595`
- `prepared/pipe-live27/host.cpp`: `4c65c915041d4d97c4f2bb638c52fb8bf956ff139bdeb63436cc831f1886f977`
- `prepared/pipe-live27/sequence.h`: `da16eff14fede51851dfc8f3446d00adc56f93702ae9557d80d3eabac1386cd5`
- `prepared/live-bridge-candidate/common.h`: `2f314da264262c3a8077c890258f25436153f456ea98da08d074f152b894d601`
- `prepared/live-bridge-candidate/admission.h`: `0cda5f7c9492fb04178bbcc911ee664288536ec21109bad679269c3535e3ba74`
- `prepared/backend-boundary24/pipe/ClientMilesPipe.cpp`: `b78fec34b28a746d18361758a6a17ab39f5093331dc3805ca6bfecc78b185167`
- `review-scratch-host29/PLAN.md`: `22752d989eec5cdd59b8555bdc4ca94e65e94b5a1df1eaddc6d8cfff241df8fc`
- `review-scratch-host29/registry_blind.cpp`: `7e5c022923981006a930f858433ae24638e7038e1269eb3cf83827c4d6f04068`
