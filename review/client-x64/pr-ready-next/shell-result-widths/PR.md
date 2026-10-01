# Retain pointer-width ShellExecute results

Os::launchBrowser and the client external-command handler narrow ShellExecute results to int before checking them. Preserve the result as INT_PTR and use the matching `%Id` diagnostic format, preventing x64 truncation. Both existing comparison boundaries remain unchanged, including the trial handler's separate `<32` condition.

This independent master-based package changes two production files (+3/-3). It contains only the status/comparison/format edits from `12bb888097a567191455f48598a6be9d87d4a257`, without that integration branch's other Os or client changes.

[Recorded native validation](https://github.com/Akilleez-QA/client-tools/blob/56ecc29fc95c62d10241b6cac0d8d9e713961db1/review/client-x64/allocator-math-next/RESULTS.md) reports eight successful Os/WinMain TU compilations across v120 Win32/x64 Debug/Release, four passing source-extracted status/format probes, and failing old-int narrowing controls in both x64 configurations. No browser was launched.

Those TU runs used integrated source/dependencies, not these complete fresh master-based files. No native build or runtime test was repeated for packaging, and no snapshot-dependent test harness is imported. The existing evidence supports the narrow status-width correction; it does not establish a full client build, browser-launch behavior, or a change to the old boundary semantics.
