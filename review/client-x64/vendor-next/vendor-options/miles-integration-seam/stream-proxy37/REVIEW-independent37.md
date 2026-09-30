# Independent shared-evidence source review — stream-proxy37

**No demonstrated correctness defect found in the added client proxy/validator code.** The justified result is a coherent client-side stream/borrowed facade with scripted transport coverage. Stable underlying sample identity is still a vendor fidelity premise; host stream/file integration remains explicitly unimplemented. Neither is established by 8,098 scripted assertions.

Read patches and test source first, then possessed SDK declarations, actual Audio uses, and existing design/contract material. This is a follow-up source-only review with shared evidence, not a fresh blind or runtime replication. Independently verified all 83 manifest entries against disk and source archive. No compiler, engine, vendor or workload execution; frozen sources unchanged.

## Source conclusions

- Open allocates its proxy and list node before the exchange. Known refusal removes the unpublished proxy; transport/decode uncertainty retains tracking and poisons the session. Null native success remains null. Duplicate identity against another live stream is rejected before publication.
- Streams own their embedded borrowed proxy. Lookup checks membership in the selected live Session before inspecting caller-supplied pointer contents. Alias replies must echo the exact parent identity; resource kinds are limited by opcode and structurally validated by the codec. A borrowed proxy from another parent cannot silently acquire the same wire identity. Confirmed close erases parent and alias together; refusal preserves them; uncertain close prevents further calls. Shutdown clears tracking only after confirmed success. No new ownership transfer or independent borrowed release is exposed.
- Exactly the five borrowed controls used by actual Audio are enabled: setters for volume, reverb and playback rate, plus volume and playback-rate getters (`Audio.cpp:3211,3212,3260,3305,3334`). Other owned-only controls remain excluded locally. The possessed 7.2a header's stream declarations (`Mss.h:5162–5206`) agree with the signed scalar and pointer shapes. All signed fields preserve bit representations; stream status remains signed.
- Time outputs use the existing v2 null/equal-pointer mask and signed result reconstruction. Unrequested nonzero slots or inconsistent aliased slots cause rejection before writes. Borrowed volume uses the shared float helper; it preserves its prior alias/copyout checks. Exception/refusal paths do not manufacture a successful SDK scalar or replay an uncertain operation.
- The cache is a stable local proxy, not a query cache: every `stream_sample_handle` call still sends a request. Once published, an altered identity or null result poisons the session instead of retargeting a live pointer. That is fail-closed behavior, not proof that the actual SDK never changes its stream sample. Neither the declaration nor Audio's repeated queries establishes stability. Existing protocol CONTRACT explicitly leaves changed native aliases requiring real evidence. Keep this restriction visible until that premise is justified.

## What the scripted count does not cover

The 256 open/close iterations dominate the repeated assertion count. They exercise sequential cycles and no cumulative operation cap; the source does not measure allocation counts or prove vendor resource reclamation. Scripted callbacks fabricate resource identities and return values, so they prove client discrimination against those values only.

Specific unexercised branches in this test source:

- No two streams are live simultaneously: duplicate stream-open identity and cross-parent borrowed-identity reuse rejection are not tested.
- Open refusal/transport loss and first alias-query refusal are not tested; malformed resource kinds, invalid structural handles and extraneous reply fields are not injected by this fixture.
- The new stream getter tests all nullable masks and unequal alias outputs, but not unrequested nonzero outputs. Borrowed volume gets only the positive aliased case here.
- The test checks borrowed release/start rejection, not the entire owned-only operation set. Prior owned34/35 tests are retained but are not compiled/run against the modified37 source by `check.py`.
- Successful close is followed by more cycles; there is no direct proxy-count assertion. Reusing freed raw handles would violate the interface lifetime contract and is not required as a pointer-ABA guarantee.

These are bounded test-coverage gaps, not independently reproduced bugs. The fixture does discriminate expected opcodes, target identity, fields, null/alias masks, parent echo, retarget/null-after-publication, and close uncertainty. The known host refusal of streams/borrowed requests is stated composition scope, not a newly discovered regression. Opcode59's new parent echo must be implemented by the eventual paired host; shared protocol version alone does not provide that implementation.
