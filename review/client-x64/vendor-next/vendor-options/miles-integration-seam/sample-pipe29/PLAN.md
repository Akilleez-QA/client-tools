# Prospective sample-pipe29 revision gate

Written before tests. Revise frozen28 only in this new directory using the same
pinned baseline and immutable native-sample27 public header. No vendor, VM,
engine, native runtime or product changes. Preserve frozen28 and parent lifetime
rejection evidence; its 379 assertions included the incorrect lifetime cap oracle.

Use a dynamic container of owned proxies, allocating proxy and container node
before remote allocation. Null allocation or known refusal removes unexposed
local storage; an unknown exchange retains it in a poisoned Session until local
abandonment. Successful release destroys its proxy. Public raw pointers cease
to be valid after release: do not promise pointer ABA detection or use fake tokens.
Private wire generations remain required; existing registry source is not proof
of integrated host/callback composition. No arbitrary cumulative allocation cap.

Shutdown forwards with live samples. Confirmed success clears local proxies;
known refusal keeps them usable; unknown outcome poisons Session and keeps state
until abandonment. Local destruction is never evidence of vendor cleanup.
Named binding remains undefined; do not invent one-bind or rebind semantics.

Acceptance fixed prospectively: retain valid frozen28 negative allocation,
resource-kind, signed output/nullability, malformed response and no-retry cases;
replace lifetime-cap and live-shutdown-refusal expectations with 256 sequential
allocate/release operations, refused-allocation cleanup, null-allocation cleanup,
and successful/refused/uncertain shutdown while live samples exist. Check local
proxy counts through private state observation, and failure before exchange on
proxy/container allocation failures. Preserve the explicit missing-binder link
control and immutable input preparation tests. ASan/UBSan scripted only. Freeze
source and identities before compilation; preserve first unexpected failure.
