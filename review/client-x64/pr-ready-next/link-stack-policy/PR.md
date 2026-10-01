# Require a resolved x64 client link and reserve two MiB of stack

Clear inherited `ForceFileOutput` for SwgClient x64 so unresolved/duplicate symbols cannot produce a forced output image. Set its stack reserve to 2097152 bytes for the exercised original PCRE recursion corpus. Stack commit size, Win32 and other executables retain their existing policy.

Two unchanged root-cause commits above native-provider head `ba1dd443249944edbe3d5a22520f6eaa84402e51`; head `5292d6fd8d07cd1d8f93091e57b1ca468c7b5833`. One property file, +4/−0; no production source, vendor or media-selection changes.

[Strict-link evidence](https://github.com/Akilleez-QA/client-tools/commit/a21af16302efa17cf1d889cd4b246fcc493c8248) records eight native metadata comparisons and actual linker commands: the existing 61 unresolved Miles imports fail with LNK1120, without `/FORCE` or LNK4088. This proves failure policy, not successful linking.

[Stack evidence](https://github.com/Akilleez-QA/client-tools/commit/dd32e5dcc392243a8f651a4d322316187ad1cf70) records the original x64 Debug corpus exhausting one MiB, completion of 24 corpus runs with the separately declared two-MiB reserve, eight native metadata evaluations and minimal-executable PE header verification. This is a bounded corpus result, not a universal recursion-depth guarantee.

These are historical integrated results, not a new build of this stack. No builds or runtime were repeated during packaging. Native-provider and source prerequisites remain separate; no whole-client acceptance is inferred.
