# Host runtime58 — one compatibility delta

Preserve host-runtime50 and native-runtime55 unchanged.55 was a valid first failure: Win32 host-thunks C4702/C2220 at the setter-only catch under /EHsc /W4 /WX.

The sole production delta removes that setter try/catch and calls the same actual SDK setter directly. Local possessed Mss.h declares extern-C linkage at319 and the setter at5239; no vendor implementation was consulted or published. The four actual callback thunks retain their existing exception boundaries unchanged. Binding publication, duplicate refusal and successful return ordering remain unchanged.

Microsoft's primary [C4702 documentation](https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/compiler-warning-level-4-c4702?view=msvc-170) specifically describes unreachable catches around extern-C calls under /EHsc in some compiler versions. This source correction preserves the exception model and /WX; it does not claim SDK fault recovery, SEH coverage, linking or runtime fidelity.

setter-only.patch is the complete production diff. Candidate paths intentionally retain host-runtime50 subdirectory names so includes/namespaces are otherwise byte-identical. No compilation or execution performed for58.
