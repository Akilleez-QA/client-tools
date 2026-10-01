# Focused source packages and review evidence

These preparation packets now have upstream submissions. Use the [complete index](../REVIEW-INDEX.md) for current heads and dependency order, and the [fork-to-upstream map](../package-inventory/fork-preparation-map.md) for the earlier fork reviews. Current source and qualification are summarized in [fork status](../FORK-STATUS.md).

| Original focused packet | Upstream client PR | Server counterpart |
|---|---|---|
| imemmove | [#25](https://github.com/SWG-Source/client-tools/pull/25) | [#37](https://github.com/SWG-Source/src/pull/37) |
| PCRE capture capacity | [#26](https://github.com/SWG-Source/client-tools/pull/26) | Client-specific package |
| ByteOrder | [#42](https://github.com/SWG-Source/client-tools/pull/42) | [#45](https://github.com/SWG-Source/src/pull/45) |
| Socket and IOCP widths | [#43](https://github.com/SWG-Source/client-tools/pull/43) | [#44](https://github.com/SWG-Source/src/pull/44) |

The [historical preparation summary](README-historical-preparation.md) preserves blind-review feedback, revisions, measured checks and review opinions. Original candidate SHAs and draft descriptions describe those stages; they are not substitutes for today's upstream PR body and head. Reviewer scores are opinions, not merge approval or runtime proof.

All other focused packets remain in their named directories. The index distinguishes production changes from test/build additions and discloses true prerequisites. Do not sum dependent PR diffs as independent source work.
