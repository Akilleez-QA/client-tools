# Handoff to build_config_next / parent

Candidate only, uncommitted. Base: 0d2f8c168165dce3e629866c76e1a697fae8318c.
Detached worktree: /home/akilleez/Work/client-wire-validation/review-fixes-next/source.
Only SwgClient Optimized|Win32 AdditionalDependencies changes: remove all occurrences of the same family as prior Debug/Release cleanup: nspr4.lib, plc4.lib, profdirserviceprovider_s.lib, xpcom.lib, xul.lib, libMozilla.lib. Debug already lacked libMozilla.lib before 94a81438; Release removed all six. Optimized has ten entries for these six names, including duplicates. Preserve every other input, configuration, path, feature and solution edge.

MemoryManager has a separate diagnostic-only %p repair. Combined patch: candidate.patch in this directory. Parent owns integration; no commit exists. Check base drift before applying. No Q/R mappings changed. Native validation uses private scratch paths only; results and limits will be recorded in README.md. No full Optimized link or product runtime acceptance is implied. No malformed allocator workloads may be run.

Final observation: parent advanced independently to `d36090a8cec01785b25bcb9608473a8b1b770c18` and is clean. Candidate remains detached at the captured starting HEAD. Read-only `git apply --check` against that parent FAILED for both files; nothing was applied. Both parent files now match the candidate byte-for-byte, indicating the repairs have independently arrived in the parent. Do not apply this patch again; verify current parent history before integration.
