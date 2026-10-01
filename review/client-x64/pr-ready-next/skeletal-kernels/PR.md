# Implement x64 hard-skinning kernels with SSE intrinsics

Add x64 implementations for the hard position/normal and position/normal/dot3 kernels, retaining the original Win32 assembly. The intrinsic path preserves the assembly's operation grouping, aligned layout requirements, iterator updates and saved MXCSR state; compile-time assertions bind the consumed layouts.

One source commit, `4f44852113e7c5dbb4a6dd3296a15f6c03d1356d`, above joint prerequisite `f56090f3178995985f23a646458c03deb6f222a5`: `SoftwareBlendSkeletalShaderPrimitive.cpp`, +97/−0. The complete file matches original `3c172d1b1`; no tooling or prerequisite source appears in the review delta.

The joint base combines published math `3c8c9099dc8962f411f9045dc7e915d21bcff31a` and UI/native-width `9396a5181497ba259c0bba0af8c2511154937088`. `SseMath.h` is a real TU dependency and needs its x64 intrinsic implementation. The width package supplies Tag's native-length fix for warning-clean header inclusion and the sibling mesh TU's Debug range types for project compilation; its other UI changes are package ordering, not kernel dependencies.

[Historical native evidence](https://github.com/Akilleez-QA/client-tools/blob/2a1ff9279341516cce2746889b29cbc6a0e8a788/review/client-x64/allocator-skeletal-next/skeletal-native-results.md) records whole-TU compilation in four configurations. Standalone whole-TU linking failed on genuine renderer dependencies and is not a runtime pass. Exact source-slice kernel comparisons produced 2688 records per Debug/Release build with zero sampled value/bounds differences across stock Win32, candidate Win32 and candidate x64, plus zero sentinel, input, iterator or full-MXCSR restoration failures.

Those integrated dependency snapshots are not a fresh build of this joint-base package. Sampled exceptional-input matches do not establish general NaN payload equivalence, all numerical inputs, renderer integration, performance or visual fidelity. No builds or runtime were repeated during packaging.
