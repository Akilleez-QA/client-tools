# Maintained media source index

Build from [`tools/miles-bridge` at `eca74ffa5741f608a1417944b2e2602868936517`](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge), not by assembling the historical candidate folders in this evidence directory. [`sources.json`](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/sources.json) is the explicit source list consumed by [`build.py`](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/build.py).

| Responsibility | Maintained source |
|---|---|
| Game-facing audio interface | [src/api/ClientMiles.h](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/api/ClientMiles.h) |
| Native backend adapters | [src/api/native](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/api/native) plus the manifest's `native` target |
| Pipe facade and session | [src/api/pipe](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/api/pipe) |
| Original provider host | [src/host/host.cpp](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/host/host.cpp) and the manifest's `host` target |
| Engine file execution | [src/file-executor/EngineFileWorker.cpp](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/file-executor/EngineFileWorker.cpp) |
| Audio selection/bootstrap | [src/dev](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/dev) |
| Game-facing movie interface | [src/api/ClientBink.h](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/api/ClientBink.h) |
| Original Bink ownership and IO | [src/host-bink](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/src/host-bink) |
| Game build selection | [client-miles-dev.props](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/client-miles-dev.props) and [link-client-dev.py](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/link-client-dev.py) |

All listed files exist in the named maintained tree. The manifest also selects the private transport, admission, buffer, file, version and EOS components. Source presence is not evidence of a particular runtime behavior; use the [current status](CURRENT-MILES-STATUS.md) for observed results and limits, and the [PR index](../../../REVIEW-INDEX.md) for submitted package heads.

The [historical experimental source index](RUNTIME-SOURCE-INDEX-historical.md) preserves earlier source selections and unresolved integration findings. Those snapshots must not be linked together as another implementation.
