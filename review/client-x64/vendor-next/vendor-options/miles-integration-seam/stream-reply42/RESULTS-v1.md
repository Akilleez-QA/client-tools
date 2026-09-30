# Malformed stream replies: first-run result

Four named scripted scenarios passed under strict C++11 warnings, AddressSanitizer and UndefinedBehaviorSanitizer: wrong stream resource kind; wrong borrowed resource kind; nonzero return on start; stray reserved result value on start. Each uses actual framing/reply validation, rejects before caller result publication, marks Session uncertain and proves no subsequent channel call.

Frozen37 implementation is unchanged, composed from frozen39 inputs. The test source includes earlier scenario definitions as support but does not execute the256cycle or other inherited tests again. This is new coverage of source-defined failure behavior, not a vendor/runtime or fullclient test. One compile/run, no failure/repair/retry. Receipt2828609c4a24f149efd88b8efcb3a38bc941ae565648bd350652cb17aba01d37.
