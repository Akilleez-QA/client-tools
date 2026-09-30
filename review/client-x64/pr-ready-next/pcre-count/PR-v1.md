# Pass the PCRE capture-vector capacity in elements

The scene command parser allocates 33 integers for capture offsets but passes sizeof(captureData), advertising 132 elements to pcre_exec. Pass the existing subscriptCount constant that declares the array extent. Pattern options and the handling of successful matches with insufficient capture space remain unchanged.

Production diff: one file, one added and two removed lines (the other deletion is a blank line).

## Validation

A prior probe against the actual PCRE 4.1 provider passed 20 checks per provider/configuration combination: zero, one and ten captures, overflowing capture counts returning zero, no match, and preserved adjacent sentinels. It never executes the old incorrectly sized call. That establishes the corrected API contract, not a game-level command test.

The isolated branch has not yet rerun that probe or the actual parser compilation. The existing external runner also needs a checkout-scoped reproducer before submission. No full x64 client link is claimed.
