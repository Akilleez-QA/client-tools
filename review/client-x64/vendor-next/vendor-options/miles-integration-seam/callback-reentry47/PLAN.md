# Prospective callback-reentry47 source gate

No test, compiler, VM or vendor execution is authorized by this packet. Parent reviews these sources before any test. No product or native direct adapter is changed.

Parents are separate: frozen callback-composition46 production file_channel.cpp (verified against its freeze-v1.json) and stream-native38 private-source-v1 pipe ClientMilesPipe.cpp. provenance.json pins both. candidate contains only two changed production TUs, the new private guard header/implementation, and one prospective test. patches are exact deltas, not edits to either frozen parent. Any later composition must retain each parent's dependency identities explicitly, not assume equal directory names imply equal dependencies.

Implementation: private POD TLS scope pointer (__declspec(thread) on MSVC, thread_local otherwise), stack scopes, no allocation on admitted guard path. requireForwardAllowed marks every active containing scope then throws a private empty C++ exception. Session::selected, request and close check first, before reading shared selection/session fields or touching proxies/channel. Invocation establishes scope inside its single-invocation lifecycle, rejects nested invocation before service entry, catches exceptions using the existing CallThrew boundary, and additionally forces CallThrew after any sticky violation. encodeCompletion already refuses that state; no fabricated SDK reply. No exception crosses a native SDK callback here.

Scopes must be created/destroyed on the same thread with ordinary stack lifetime and strict LIFO unwind; they are noncopyable and are not an ownership/scheduling mechanism. Nested scope construction marks containing invocations failed even if nested failure is swallowed. Success never resets an ancestor's failure. A callback can catch a rejected call and return, but its invocation still cannot encode success. Its file side effects remain uncertain and require the existing owner failure retention path.

Session construction/destruction, its diagnostic/helper methods and raw Channel access remain private composition operations, forbidden from callbacks. Channel bootstrap already precedes Session selection, so guarding only the constructor body would be too late to authorize bootstrap. The composition root must establish/tear down Session on the owning thread outside callback scope; this candidate does not add a constructor admission or arbitrary cross-thread synchronization scheme. All public pipe forwarding functions inspected use selected(); request/close additionally guard internal bypass. A future public/direct-channel path needs the same pre-access check. Do not claim general callback-created-thread cycle detection.

Prospective tests.cpp scenarios (one run, no repetition inflation):

* Actual public startup, private request and close from invocation scope reject before scripted Channel call/finish; selected session state remains unchanged.
* Actual selected Invocation normal callback encodes a reply; callback swallowing a facade guard exception yields CallThrew and unchanged rejected output frame.
* Callback throwing independently yields CallThrew; TLS restored after each case.
* Nested scope marks parent sticky, and a nested actual Invocation never calls its service.
* Two simultaneous threads: one holds callback scope while the owning thread successfully calls actual pipe startup; this rejects process-global suppression.
* Exceptional scope unwind restores allowed forwarding.

The scripted Channel is only an observation counter, not SDK behavior or runtime evidence. Test includes actual modified pipe and actual modified Invocation. A later authorized strict portable gate should compose the dependencies pinned by the two parents, build tests.cpp + invocation_guard.cpp + ClientMilesPipe.cpp + file_channel.cpp + required real codec/reply dependencies under C++11, -Wall -Wextra -Werror -pedantic, ASan/UBSan and pthread, then run once with bounded timeout. Preserve first compile/test failure with no automatic repair/rerun. Native v120 compatibility is a design target (throw(), private copy declarations, POD TLS), not checked by this source-only packet. No native plan or compiler authorization is implied.

Not established: operational host failure termination, live SDK callbacks, actual engine TLS, arbitrary reentry support, concurrent Session access safety, or production adoption. The guard is an explicit unsupported pipe boundary, not a claim that canonical callbacks never reenter.
