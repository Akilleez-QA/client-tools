The client-facing Miles API needs a direct-provider implementation so that selecting a process boundary does not change the caller interface. Implement the ClientMiles declarations with native ABI/callback adapters, startup and file-callback registration, and the existing exception-to-fatal boundary.

**Depends on #41 (contracts).** This master-based branch contains only this component: 15 production files, +945/−0. It includes no pipe backend or game selection. Native and pipe facades are alternative targets.

Compiling the native target requires the genuine Miles SDK and matching provider/toolchain. No SDK headers, libraries or binaries are redistributed.

These are dormant additions: no existing project, backend selection or workflow changes. Build entry points and game integration are separate follow-ups. The individual branch does not build or enable audio by itself. Existing native/component results used the integrated implementation; no new runtime test was performed on this isolated package.

[Source identity and composition verification](https://github.com/Akilleez-QA/client-tools/blob/ef190a47e431ffa58dfba01d81e0a73e07fa96bf/review/client-x64/package-inventory/upstream-delivery/miles-additions/README.md): all introduced files retain the reviewed blobs. Merging contracts and the five component branches reproduces the complete reviewed pre-Bink tree exactly. That is source-composition evidence, not a new build or a claim of audio fidelity or shutdown acceptance.
