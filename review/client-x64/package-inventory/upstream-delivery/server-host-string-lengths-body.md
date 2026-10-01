Draft pending the existing [server CI repair (#38)](https://github.com/SWG-Source/src/pull/38). The source change applies independently to `master`; this PR does not duplicate that workflow repair. Master’s inherited clone/checkout failure is not evidence about this candidate. No successful upstream CI run is claimed.

Keep duplicate-string allocation lengths, lowercase-copy indices and tag-conversion string lengths as `size_t`. This removes narrowing of `strlen` results to `uint` or `int` while preserving null handling, allocation policy, lowercase conversion and the existing first-four-character tag encoding with space padding.

Two source commits, two production headers, +5/−5, directly above upstream `master`. The duplication and tag helpers do not call `imemmove`; that repair and the CI change are excluded. All changed source hunks and their surrounding context match the reviewed fork package. Misc.h has a different whole-file hash because the unrelated move-helper change is absent. No tests, vendor files or build metadata are added.

The [duplicate-string change](https://github.com/Akilleez-QA/src/commit/c98f2a6dca7794ec8a2f1705208b2796f25c981f) follows the already host-sized client helpers. The [tag-conversion record](https://github.com/Akilleez-QA/src/commit/c03e4a1a72c3f5daff8501907e4bfc70e1919fa1) describes historical client native Debug consumer compilation and 4,098 sampled tags on both ABIs. This is supporting component evidence, not an exact build of these server headers: server `Tag.h` retains different null-diagnostic wording, and `Misc.h` retains server `nullptr` conventions and its existing move-helper overload.

No new build or runtime check was performed during packaging. Giant inputs, allocation failure, arbitrary character conversion and full server behavior are not newly qualified. The existing `tolower` input contract remains unchanged. These are host-memory lengths; wire formats and tag byte order are unchanged.

[Review packet and exact source identities](https://github.com/Akilleez-QA/client-tools/blob/de951450e45a8caf37cf3b8cea691aad36c75e54/review/client-x64/pr-ready-next/server-host-string-lengths/RESULTS.md).


Upstream review identity: base `7d2159a337281184d6a55db30d2bc9a4013c0e80`, head `9cf3ef1e7608e20473e05ad92cd426367f57488b`.
