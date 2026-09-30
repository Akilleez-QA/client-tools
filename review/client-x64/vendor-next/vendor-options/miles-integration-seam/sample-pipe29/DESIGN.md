# Sample client ownership revision29

This is an unapplied overlay on the pinned pipe-native26 baseline. It implements
four of the immutable native-sample27 public operations through the existing
Session/Channel and reply decoder. Named-file binding remains undefined; the
full sample_time helper must still fail to link. No real host is added.

Frozen28 is unsuitable for native-shaped allocation: its tombstones consumed a
64-allocation session lifetime budget. Parent independently reproduced 64 complete
allocate/release pairs followed by rejection before the 65th request in
../sample-pipe28/parent-lifetime-review/result.json. Its original passing test
explicitly required this wrong limit. Its live-sample shutdown guard also added
a caller precondition absent from actual Audio.cpp1437 shutdown policy;
getSampleTime4437–4455 releases only on bind success. Frozen28 evidence is intact.

Revision29 uses a list of owned proxy allocations. Both proxy and list node are
allocated before remote exchange; publication to the application occurs only on
a successful non-null reply. A known refusal or successful null result removes
the unexposed entry. An uncertain exchange keeps it until poisoned Session
abandonment. No cumulative cap or released tombstones are retained. Allocation
failure has the ordinary allocator limit and happens before the remote operation.

Confirmed release destroys the local proxy. Public raw HSAMPLE values become
invalid on release; using one afterwards violates the native lifetime contract.
Allocator reuse is allowed, and arbitrary public stale-pointer ABA detection is
not promised. No fake pointer token or narrower one-bind policy is introduced.
Current owned identities are compared before dereferencing caller memory.
Private wire identity remains kind/slot/generation, never the proxy address.
Existing ResourceRegistry source increments generations and rejects stale wire
handles, but host allocation/release and callback ownership are not integrated
here. Their runtime generation correctness remains a required future proof.

Shutdown issues the existing request while samples exist. Known refusal preserves
local ownership and running state; unknown completion poisons Session and keeps
local state until abandonment. Confirmed success clears all proxies and marks
stopped. No destructor retries or synthesizes remote cleanup. Clearing local
proxies does not prove host registry, retained-buffer or vendor teardown.

The signed query masks and decoder checks are retained. Neither requested output
is written until accepted result validation completes. Same-pointer outputs are
assigned total then current; vendor alias fidelity is unverified. A remote
InvalidResource still maps to the existing InvalidDriver FailureReason. No public
error API change is included.

The unchanged private PreparedInput primitive copies sealed image and suffix via
BufferUpload/RetainedBuffers. It makes no vendor call and establishes no bind,
failed-bind, rebind or retirement semantics. Actual buffered sound/music callers
reuse the same sample after stop/end, so global one-bind restrictions are invalid.
The remaining dependencies are binary/sealed upload transport; actual host sample
allocation and transactional publication; release/callback quiescence and wire
generation integration; and vendor-backed ownership for binding and replacement.
No portable mock result is evidence those integration steps are complete.
