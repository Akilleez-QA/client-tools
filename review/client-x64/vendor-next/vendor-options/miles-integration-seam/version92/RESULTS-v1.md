# Observed portable version92 result

Parent ran the pre-reviewed frozen gate once. Compilation and all seven isolated process modes exited zero, with no compiler/sanitizer diagnostics; all 26 frozen inputs remain unchanged.

| Mode | Assertions |
|---|---:|
| normal | 277 |
| oversize | 47 |
| nonterminated | 47 |
| missing | 47 |
| legacy_text | 47 |
| callback | 47 |
| context | 47 |

559 assertions in this run. These are bounded checks of actual version90 Core/Session/query/reply code using the declared scripted Channel and unavailable Runtime substitute. Malformed replies preserved caller bytes and failed before the scripted settlement checkpoint. This is not an actual LiveChannel ACK, Windows resource, vendor, ABI, engine, or shutdown test. Source review and the earlier native resource observation remain distinct evidence. Raw command lines, logs and result JSON are retained under evidence-v1; private produced executable is excluded from publication.
