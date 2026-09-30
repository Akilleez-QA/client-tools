# Revision 4 prospective directory discrimination

Preserve the frozen v3 packet. This iteration changes the test only: dispatch both valid private `.` and `miles` paths, each after resetting the SDK to the other path, and compare each immediately copied response with its direct-call expectation. End at `miles` before startup. SessionInputs and direct path storage remain alive through shutdown. Production component source is unchanged.

Prediction: genuine original DLL yields 35/35 in x86 Debug and Release. A private source mutation hardcodes `miles` at the directory vendor call; it must fail the `.` comparison only, yielding 34/35 and exit1, while normal preference restoration/shutdown still runs. Any other outcome is preserved, not relabeled.

Build a fresh native v120 six-entry matrix: portable tests both ABIs/configurations, host x86 both configurations. Capture source/header/tool/library identities before and after compilation and PE hashes immediately after link; verify the pinned receipt before execution. Reuse the bounded original-DLL private-prefix/null-sink setup; no playback, samples, streams, callbacks, engine fixture or product changes. No vendor files are published.
