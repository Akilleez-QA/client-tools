# Text packet contract

`packet-manifest.json` is a flat JSON object mapping packet-relative POSIX paths to `{ "bytes": integer, "sha256": lowercase-hex }` records, matching the backend-boundary24 packet format. Its path base is this backend-live25 directory, also the root of packet-v1.tar. There is no schema discriminator field. The archive includes every manifest member plus the manifest itself; the manifest does not hash itself.

The allowlist is local authored Python/Markdown/YAML, .gitignore, source-manifest.json and retained native/runtime .json/.log/.cmd/.sha256 evidence. No executable, object, DLL, plugin, Wine prefix, asset, SDK body or nested binary archive is included. Frozen shared source is identified by source-manifest.json and the separately retained source archive pin, not duplicated here. The source manifest uses source-archive-relative paths; its revision4-tools paths map to the existing live-bridge-candidate helper directory in the seam.

The separate backend-zero-startup25/packet-manifest.json uses the same flat records and its own directory as path base. It contains only that test-only source, plan/report and pure-test text evidence.
