# A: upstream-based Release link cleanup

Review branch `x64-link-cleanup`, head `46a56f6a5219932ab2567970c79144570b97ac36`, contains one commit on upstream `94945103`: `build: remove unused explicit SwgClient Release link inputs`. Diff: one project file, +1/-1 XML lines, removing 74 semicolon-separated entries. No source code, diagnostic instrumentation or wire/DPVS commits are included.

## Native product validation on the actual PR base

On the Windows VM, after the earlier copy/build had completely finished, extracted the exact upstream archive `C:/pr-link-base.tar` again into `C:/pr-link-review`. Built the unmodified upstream SwgClient Win32 Release product, saved its executable, replaced only its project file with the branch version, rebuilt and saved the resulting executable. A full SHA-256 audit verified all 20,501 tracked guest files against upstream Git blobs, with zero mismatches. The accepted baseline then used `SwgClient:Rebuild`, recompiling the client and its solution dependencies so stale seeded objects cannot carry the earlier copy race into this result. Original third-party binary libraries remain the upstream inputs.

Both runs used native VS2013 v120 and MSBuild 12:

```
MSBuild.exe src/build/win32/swg.sln /t:SwgClient:Rebuild /m:2 /p:Configuration=Release /p:Platform=Win32 /v:normal
# After replacing only the project file:
MSBuild.exe src/build/win32/swg.sln /t:SwgClient /m:2 /p:Configuration=Release /p:Platform=Win32 /v:normal
```

| Product | Exit | Errors | Warnings | Executable bytes |
|---|---:|---:|---:|---:|
| upstream `94945103` (clean rebuild) | 0 | 0 | 170 | 29,016,064 |
| upstream + link cleanup | 0 | 0 | 30 | 29,016,064 |

`compare.py` reports `normalized_equal: true` for the complete executable, normalizing only parsed COFF/export/debug timestamps and PDB age. `.text`, `.data`, resources and relocations are already identical without normalization. The raw `.rdata` comparison differs because it contains normalized metadata; this is not an unaccounted code/data difference. Known diagnostic log markers are absent. Published logs are UTF-8 conversions of the retained original UTF-16 records. The warning count is not zero; runtime/default-library and missing vendor PDB warnings remain outside this cleanup.

Project file SHA-256 values match the local Git blobs:

- upstream: `46129c5f486d3c18b5f96832199bd183af9c467648bd8d33efaf6be3c7ad0cbe`
- branch: `e8b291e5bc649e31672f8c91a6828d0f650116a297432a103945abe99584564e`

Executable SHA-256 values:

- before: `ecca5d8c5d3a89a390925066a9e8f97551aac05250bd80b718cc00bf3369ac58`
- after: `2da5aef0069812eb2875b1b181e0763036531c8bcf4e3c205e4641561793cab5`

These upstream-based files differ in size from the earlier product proof on the wire/DPVS-based branch (29,017,600 bytes). Do not substitute one proof for the other; both comparisons independently establish equality within their respective before/after pair.

## Evidence and limits

- `rebuilt-before.log`, `rebuilt-after.log` and `.exit` files: accepted native product build records (4m41.53s clean baseline; 17.40s after relink). The 170 versus 30 warning counts reflect compilation plus linking versus relinking, not a claim of 140 warnings fixed.
- `base-manifest.json`, `tracked-source-verification.json`: all 20,501 tracked source/input files verified against base Git blobs before building.
- `verified-*` and `incremental-comparison.json`: earlier incremental proof, retained as supplementary only.
- `verified-*-project-hash.txt`: guest project identity.
- `compare.py`, `comparison.json`: whole-PE comparison method and result. The accepted `product-before.exe` and `product-after.exe` (also named `rebuilt-before.exe` / `rebuilt-after.exe`) are retained locally, not published; rerunning the comparison requires rebuilt binaries.
- `removed-groups.json` and `PR-A.md`: the 74 exact removed names, grouped for review.

Release only. Debug and Optimized require independent comparisons before cleanup. The commit message already states that scope and rationale. Static output equality does not show that dynamically loaded libraries or source-level default-library directives are unused. No vendor feature is stubbed or removed. The 67 uncommitted configuration files are not part of this branch. The source branch is published for review; no PR was opened.
