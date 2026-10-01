Reverse Miles callbacks must stay associated with the session that admitted them. Add engine-worker invocation jobs, the admission coordinator, session file owner, host association mapping and the client file/EOS callback runtime. Their ownership chain carries work and completion through the admitted session.

**Depends on #41 (contracts) and #48 (file transport).** This master-based branch adds 14 production files (+1589/−0) and the existing engine-worker context and lock-admission test files (+209 lines), 17 files total.

Engine-worker compilation requires the real engine headers and settings. The included context files support the test; they are not a replacement production thread/TLS implementation.

These are dormant additions: no existing project, backend selection or workflow changes. Build entry points and game integration are separate follow-ups. The individual branch does not build or enable audio by itself. Existing native/component results used the integrated implementation; no new runtime test was performed on this isolated package.

[Source identity and composition verification](https://github.com/Akilleez-QA/client-tools/blob/ef190a47e431ffa58dfba01d81e0a73e07fa96bf/review/client-x64/package-inventory/upstream-delivery/miles-additions/README.md): all introduced files retain the reviewed blobs. Merging contracts and the five component branches reproduces the complete reviewed pre-Bink tree exactly. That is source-composition evidence, not a new build or a claim of audio fidelity or shutdown acceptance.
