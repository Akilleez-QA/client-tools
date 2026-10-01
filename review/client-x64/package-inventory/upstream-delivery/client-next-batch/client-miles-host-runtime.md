The 32-bit Miles host must retain ownership of native handles and reverse callbacks across client requests. Add its native backend, dispatcher/resolver, entry point, SDK file/EOS callback trampolines, upload bindings, metadata/version queries and reverse callback runtime.

**Depends on #41 (contracts), #48 (file transport) and #49 (client callbacks).** This master-based branch adds 14 production files (+1568/−0) and the unchanged upload-binding test (+205 lines), 15 files total.

The host file runtime retains the reviewed process-owned lifetime repair: paired stop does not authorize destroying that runtime. Building the host requires the genuine Miles SDK/provider. No vendor headers or binaries are redistributed.

These are dormant additions: no existing project, backend selection or workflow changes. Build entry points and game integration are separate follow-ups. The individual branch does not build or enable audio by itself. Existing native/component results used the integrated implementation; no new runtime test was performed on this isolated package.

[Source identity and composition verification](https://github.com/Akilleez-QA/client-tools/blob/ef190a47e431ffa58dfba01d81e0a73e07fa96bf/review/client-x64/package-inventory/upstream-delivery/miles-additions/README.md): all introduced files retain the reviewed blobs. Merging contracts and the five component branches reproduces the complete reviewed pre-Bink tree exactly. That is source-composition evidence, not a new build or a claim of audio fidelity or shutdown acceptance.
