# Preserve Windows socket handles and IOCP keys at pointer width

Windows x64 socket handles and IOCP completion keys are pointer-width values. Three local SOCKET declarations and Sock's stored handle currently narrow them to 32 bits; both TCP completion handlers also pass a 32-bit output to GetQueuedCompletionStatus. Use uintptr_t/SOCKET for the handles and ULONG_PTR for completion keys. Transferred-byte counts and socket operation results stay 32-bit.

This is five production files (+9/-6), stacked on the separate [memory-move prerequisite PR37](https://github.com/SWG-Source/src/pull/37) at `1481143ca4f033ef979faff52a4d03bb8d636292`. It carries no Linux, clock, serialization, or LP64 PR35 changes. Rebuild affected Windows x64 libraries and consumers together because member/signature layouts change.

The [client counterpart's recorded Windows checks](https://github.com/Akilleez-QA/client-tools/tree/3197e7ee0c20321dfb5bc9efb11c8b8ec2f1fb90/review/client-x64/pr-ready-next/socket-widths/revision2) cover the same API-width corrections: 100 accepted compiler outcomes, 60 raw API executions and 1,260 assertions, with high-bit IOCP keys and reverted-key compile controls. Those are supporting client results, **not an exact-server native build or runtime result**; the server source files and build layout differ. This local package has not yet run a server-owned Windows compile check.
