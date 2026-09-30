# Strict x64 link policy

Candidate clears inherited ForceFileOutput only for x64 SwgClient. The installed VS2013 v120 link.xml enum has Enabled, MultiplyDefinedSymbolOnly and UndefinedSymbolOnly; empty metadata means no /FORCE switch. There is no Disabled enum.

Eight native metadata checks preserve Win32 Release empty and Debug Enabled, and x64 Release empty. Only x64 Debug changes Enabled to empty. Actual native MSBuild Link task emits /FORCE before the change and omits it after. Both runs report the identical 61 unresolved Miles symbols. Baseline produces an invalid image and LNK4088; candidate terminates with LNK1120. Neither executable was run.

Both MSBuild invocations return 1 because the task parses LNK2019 errors even when the forced raw linker returns success. Earlier direct-link replay returned 0 under /FORCE; this is a raw-linker false green, not proof MSBuild itself passed. Acceptance checks must inspect diagnostics as well as process status.

These are isolated native linker-task experiments using preserved 91dc inputs plus documented genuine provider and capture candidate libraries. They are not a current-head full build. v1 failed on unsupported nested response-file packaging; v2 fixes diagnostic packaging only.
