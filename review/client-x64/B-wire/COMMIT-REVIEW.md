# Wire commit-message review

The 13 commits are retained as existing published history. This review does not rewrite them.

- `ae51d0a6` and `b5bb8792`: their stated portable passing counts were reproduced independently with each commit's own runner and fixtures. The stock comparison for the final suite was reproduced with the `b5bb8792` runner and `94945103` production sources.
- `f87084a3`: "every serialized container count fit its field" on Win32 is too broad. Signed 32-bit count fields cannot represent `size_t` values above `INT32_MAX`, even on Win32. New rejection behavior deliberately changes that oversized-input boundary. Likewise, testing signed count overflow requires more than `INT32_MAX` elements, not necessarily more than 2^32.
- `ae51d0a6`: the historical "16 call-site edits" describes the Archive group; the complete mirrored generic-count patch has 18 sites including the two external sites. Do not present 16 as the complete count.
- `e4e6b7f1`: "Close the coverage gaps" covers its listed fixtures, not all wire messages. The final README lists the uncovered messages and compile-only writers explicitly.
- Early commits intentionally include superseded signed-counter, unsigned-timestamp and FATAL-policy implementations; later commits repair them. Their individual test counts describe those historical fixtures, not the final branch's acceptance suite. They should not be presented as independently complete migration checkpoints.
- Older server-state statements and per-developer MSVC flag caveats describe the date of those commits. They are not assertions about current upstream server state.

The PR description must say "legacy bytes preserved for tested representable values", not that all Win32 behavior is unchanged. Oversized count rejection is an intentional behavior change. The independent reruns do not reproduce every historical negative-control claim in all 13 commit messages.
