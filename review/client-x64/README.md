# Client/server x64 review packet

**58 upstream PRs are submitted: 46 client and 12 server.** Start with the [current fork status](FORK-STATUS.md) and [complete PR index](REVIEW-INDEX.md), verified against GitHub on 2026-10-01.

| Review task | Start here |
|---|---|
| Find each PR, its head, size and dependency order | [Submission index](REVIEW-INDEX.md) |
| Match an earlier fork draft to its upstream submission | [Preparation map](package-inventory/fork-preparation-map.md) |
| Find the maintained implementation and test limits | [Fork status](FORK-STATUS.md) |
| Inspect source/build accounting | [Package accounting](package-inventory/remaining-units.md) |
| Review the temporary Miles/Bink backend | [Media status](vendor-next/vendor-options/miles-integration-seam/CURRENT-MILES-STATUS.md) and [maintained source index](vendor-next/vendor-options/miles-integration-seam/RUNTIME-SOURCE-INDEX.md) |
| Read the original link, wire and DPVS preparation | [Historical packet introduction](README-historical-before-upstream-delivery.md) |

The client has linked and run in the bounded environments recorded in the evidence. Earlier reports saying it stops at unresolved Miles imports are historical. Current server upstream checks pass; upstream client checks are absent, so client qualification remains the named native/fork evidence. Maintainer review, merging and broader fidelity acceptance are separate.

This branch publishes evidence and review navigation, not executable releases. Build the exact source branch identified by a PR or result. Historical failures, numerical limits and original logs remain available; no SDKs, provider binaries or game assets are supplied here.
