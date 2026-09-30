# Private callback protocol48 portable result

First strict Clang C++11 ASan/UBSan gate passed all eight named scenarios. Build/run exits0, no build diagnostics, frozen sources unchanged. Raw run reports8085 assertions; many are per-byte sentinel/truncation checks, not distinct behavioral scenarios.

The independent literal-byte oracle covers install/reply/consumption-ACK fields; malformed/context/length/version mutations and output-preservation checks passed. Stream alias success preserves its original-parent echo including null aliases. Private version3 rejects previous versions. No generic SWG wire change occurs.

ACK validation here is stateless: duplicate bytes may validate twice, while actual one-time owner settlement is a separate control integration obligation. Installation echo reports a correlated status; it does not prove an SDK call. No endpoint, vendor, native Windows runtime or engine work ran.
