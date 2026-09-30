# Four sample operations in the existing pipe composition

This is an unapplied client overlay and a private input preparation primitive.
It is not a complete pipe implementation of ClientMilesSample.h. The public
native-sample27 header is copied byte-for-byte into the isolated test stage.
`set_named_sample_file` deliberately has no pipe definition, so the complete
duration helper fails to link. No production or frozen file is changed.

## Implemented state and data flow

The overlay extends pipe-native26's existing Session, ClientMilesPipe.cpp and
StartupBridge::decodeReply. LiveChannel can use that same decoder; its framing,
request correlation, process ownership and sticky exchange-failure path are not
replaced. No new Channel interface or hook table is introduced.

Each allocated local HSAMPLE is a typed OwnedSample proxy owned by the selected
Session. Before allocation is sent, both proxy storage and its container entry
exist. A remote null allocation yields null and frees its never-published proxy.
A returned owned-sample handle publishes the existing proxy. BorrowedSample and
other resource kinds are rejected by the real reply decoder. No stream alias
conversion is provided. Arbitrary caller pointer values are compared with the
owned list before dereference.

Confirmed release marks the proxy dead, retaining its address as a tombstone.
A second release, end or query is refused locally. New allocations receive a
different local address for the rest of that Session. The 64-entry lifetime
budget is explicit: released tombstones still count; exceeding it fails before
a remote call. This bounded prototype resource policy is not a claim of unlimited
native allocation equivalence. All pointers expire at Session destruction;
cross-session stale-pointer use is outside the public lifetime contract.

Queries encode mask bit0 for total and bit1 for current; the decoder accepts only
the two signed scalar slots. The caller layer additionally rejects nonzero values
in unrequested slots. It writes no output until the complete reply is accepted.
The same-pointer case writes total then current, matching the argument order; a
transport cannot reproduce intermediate writes or output changes after a failure.
Null pointers remain null requests and are never dereferenced locally.

Channel throw, unknown status, invalid typed reply or invalid requested-output
shape makes Session uncertainty terminal. No allocate, release or query is retried.
Confirmed release alone retires a live local identity. Unknown release cannot be
treated as successful cleanup. Shutdown is refused while a sample is still live;
faulted Session teardown still relies on the existing process owner rather than
inventing a vendor release. Existing FailureReason::InvalidDriver still maps a
remote InvalidResource status; the public error enum is not changed by this patch.

## Host integration still required

Host27 has a fixed 22-request fixture oracle, and Backend owns startup/driver
shutdown. Its sample allocation and release paths are absent. Existing generic
host dispatch can query/end OwnedSample, but it cannot own allocation/publication,
input lifetime or release. A future host extension must share Backend's registry
and resolver, not invent a second registry or startup owner.

An allocated vendor sample must become an OwnedSample registry entry with a
nonzero slot/generation; stale generations must resolve to nothing after release.
Registry insertion can allocate, so native allocation followed by fallible
publication needs a concrete recovery policy or pre-reserved registry slot.
Neither is implemented here. On successful release, retire only after the actual
release returns and relevant callback references are quiescent; this slice enables
no callbacks. Refuse driver shutdown while samples exist, unless a separately
proved ordered teardown accounts for all of them. A lost response requires
session/process abandonment handling, not a repeated native operation.

These host changes, including strict request validation and result formation, are
required before the client overlay is usable on real pipes. The scripted Channel
in this gate is explicitly not that host implementation.

## Named binding and rebinding dependency

Protocol API-MAP specifies target Sample, resource sealed Buffer, text suffix,
value0 U32 file size and value1 S32 block. The current Channel cannot send binary
upload chunks. BufferBegin/Chunk/Seal/Release, their budgets and upload authority
must be connected to the existing Session before that path can be implemented.
The adapter must preserve the full signed block and bind scalar result, not
reduce it to a boolean or silently change a failed bind into success.

PreparedInput uses actual BufferUpload and RetainedBuffers to construct two
stable, bounded, immutable copies. Its aggregate limit includes the suffix NUL.
Preparation can temporarily hold an extra image copy while staging, so peak
preparation memory can approach twice the image limit. The original upload is
additional storage owned by its existing session budget. This primitive makes no
SDK call, publishes no sample association, and infers no vendor quiescence.

Real callers invalidate a one-bind restriction: Audio.cpp's buffered sound/music
paths reuse the same sample after stop/end and bind again (5333–5338,5353–5358).
The temporary duration helper instead releases only after successful binding
(4437–4455), with a preexisting failure-path cleanup gap. Those policies cannot be
collapsed into the same one-bind experiment and called native compatible.

Before defining the pipe binder, determine the actual SDK's ownership after bind
success, bind failure and replacement; whether old and proposed image/suffix
references can coexist; and which observed operation ends each reference. The
owner then needs a bounded replacement transaction preserving both sets until
the corresponding proof permits retirement. Retaining every attempt forever
neither implements replacement nor yields acceptable bounded fidelity. This
gate leaves the function unimplemented rather than invent those rules.

## Evidence boundary

Portable tests exercise the actual staged Session/decoder with encoded scripted
responses, plus preparation using actual local helper implementations. They do
not exercise SDK calls, an engine file, real IPC, host registry generation, vendor
retention, native ABI, playback or audio fidelity. A passing result qualifies only
the tested source subset and must retain the missing-bind link failure.
