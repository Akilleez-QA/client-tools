Calls across the Miles process boundary need explicit file-token and reply ownership. Add Windows endpoint/bootstrap support, the file request protocol/channel, callback signatures, opaque file tokens, services and invocation guards. Reply transactions distinguish preparation, send, consumption and acknowledgment before exposing a result.

**Depends on #41 (contracts).** This master-based branch contains only 20 new production files, +1331/−0. The native facade is not a direct include prerequisite.

The Audio admitted-callback header is a declaration here; its engine implementation and project adaptation follow with the Audio integration. Engine-worker admission, client callback ownership and host dispatch are separate packages.

These are dormant additions: no existing project, backend selection or workflow changes. Build entry points and game integration are separate follow-ups. The individual branch does not build or enable audio by itself. Existing native/component results used the integrated implementation; no new runtime test was performed on this isolated package.

[Source identity and composition verification](https://github.com/Akilleez-QA/client-tools/blob/ef190a47e431ffa58dfba01d81e0a73e07fa96bf/review/client-x64/package-inventory/upstream-delivery/miles-additions/README.md): all introduced files retain the reviewed blobs. Merging contracts and the five component branches reproduces the complete reviewed pre-Bink tree exactly. That is source-composition evidence, not a new build or a claim of audio fidelity or shutdown acceptance.
