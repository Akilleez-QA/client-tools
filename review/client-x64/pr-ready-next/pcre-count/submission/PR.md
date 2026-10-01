# Pass the PCRE capture-vector capacity in elements

The scene animation parser allocates 33 integers but passes `sizeof(captureData)` to `pcre_exec`, advertising 132 integer slots. Pass the existing `subscriptCount` array extent instead. Pattern handling and zero-result match behavior are unchanged.

The production change is one file, +1/−1. Source, regression tool and CI are separate commits. The [PCRE caller structure workflow](https://github.com/Akilleez-QA/client-tools/actions/runs/36828791977) passed on this head: it checks lexical caller structure and rejects an in-memory reversion to the unsafe byte-count argument. Hosted CI does not execute PCRE.

[Recorded native results](https://github.com/Akilleez-QA/client-tools/tree/3197e7ee0c20321dfb5bc9efb11c8b8ec2f1fb90/review/client-x64/pr-ready-next/pcre-count/revision2/native-text/pr-pcre18-revision2/results-final) report 25/25 safe provider checks in six configurations: source-built PCRE 4.1 on Win32/x64 Debug/Release and the original library on Win32 Debug/Release. The tested caller at `1df8947d` differs only by the original final newline restored here; probe and runner are byte-identical. The native matrix was not repeated for that formatting change.

[Caller compilation evidence](https://github.com/Akilleez-QA/client-tools/tree/3197e7ee0c20321dfb5bc9efb11c8b8ec2f1fb90/review/client-x64/pr-ready-next/pcre-count/revision2/native-text/pr-pcre18-tu) covers four configurations using existing external project metadata; x64 needs separate development headers/configuration and reports four C4267 warnings per configuration. This is not an exact-branch full client build or game-command test. The unsafe original call is never executed by the regression.
