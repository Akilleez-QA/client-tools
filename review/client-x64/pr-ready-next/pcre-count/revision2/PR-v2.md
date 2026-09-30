# Pass the PCRE capture-vector capacity in elements

The scene command parser allocates 33 integers for capture offsets but passes `sizeof(captureData)`, advertising 132 elements to `pcre_exec`. Pass the existing `subscriptCount` constant that declares the array extent. Pattern options and handling of zero (a successful match with insufficient capture storage) remain unchanged.

Adds a checkout-scoped regression tool requiring an explicit real PCRE 4.1 header and static library. A lexical source assertion binds the reviewed caller declaration and argument; a safely reverted byte-count expression is rejected before provider execution. The separately compiled runtime probe always uses the correct bounded capacity, never the old overflowing call. Failures, missing inputs and unexpected pass totals return nonzero.

Validation: 25/25 checks per configuration with genuine source-built PCRE 4.1 on Win32/x64 Debug/Release, and 25/25 with the original repository library and header on Win32 Debug/Release. Checks cover 0/1/10/11/20 captures, successful capture truncation, whole-match offsets, no match and adjacent sentinels after both calls. Exact provider/header/caller hashes, commands and logs are recorded in the evidence packet; the checkout README documents reproduction without developer-specific paths. No vendor binaries or headers are added.

The exact caller also compiled in all four native configurations using existing external project metadata and real headers, with PCH reuse disabled. This is not a clean build of the isolated PR branch: x64 depends on separate development configurations/headers and still emits four C4267 warnings per configuration. No full client link, game-command execution or wider regex grammar claim is made. Structural source binding is explicitly separate from runtime API-contract evidence.

Final review head: `1df8947d7971567c014e8e4815f95ac64b5f9963`; production remains `85cd72af`. The final native runner/probe hashes match the committed files.

[Native evidence, commands and independent review packet](https://github.com/Akilleez-QA/client-tools/tree/review/client-x64-evidence/review/client-x64/pr-ready-next/pcre-count). Prepared on the working fork; upstream submission and final target branch remain subject to owner approval.
