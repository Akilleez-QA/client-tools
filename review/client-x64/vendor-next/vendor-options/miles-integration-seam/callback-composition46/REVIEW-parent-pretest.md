# Parent pretest review

Read the complete production provenance/diff, new composition fixtures and first runner before execution. The source path correctly passes FileServices from the retained table through context, owner, job and Invocation; no global selected-table fallback was introduced. All production files derive unchanged from44/45.

Found a test prediction error before any test ran. After a valid mapper envelope is rejected by SessionFileOwner before its local intake advances, the mapper intentionally retains its correlation row and fails the session. The next mapper request uses intake2 while the owner still expects1, so it is Rejected again, not FailedUnanswered with a new owner operation. This is the documented terminal intake skew, not a recovery path. The corrected test must require mapper rows retained, no owner operations and no new file execution. Earlier pretest freeze metadata should remain distinguishable from the revised first-gate manifest.

The runner also needs a post-run input-hash check and exactly one appearance of each named scenario. Exit0 alone would not detect later omission of a test group. Requested these changes before execution; no production source repair or test rerun occurred.

This review does not authorize native execution, engine tests or product adoption. The scripted job continues to substitute for Windows worker/event behavior explicitly. A valid runtime delivery still needs continuous pipe ownership, actual host callbacks, termination and fidelity evidence.
