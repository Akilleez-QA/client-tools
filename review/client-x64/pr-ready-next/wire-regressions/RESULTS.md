# Wire regressions

Candidate `d8cb69a4b50fbbb23e09a8cc6bc97cedc6d9a185`, prerequisite `085a62e3358e7b51c5198c93bb1581864020c3fb`. [Description](PR.md), [file identities](receipt.json), [independent review](INDEPENDENT-REVIEW.md). No production changes are in this package.

The [composed portable workflow](https://github.com/Akilleez-QA/client-tools/actions/runs/36850510021) passed at 505795c7dd132b88d282151d8c95de999d1f45ba: 71/78 wire results, 85 ByteStream and 34 decoder checks per ABI, 12 ownership checks, 298 EOS/1,047 Bink protocol/22 video-admission checks. That explicit composed base includes these test inputs; it is not a native-MSVC, original-provider or full-client result. [CI packet](../regression-ci/RESULTS.md).
