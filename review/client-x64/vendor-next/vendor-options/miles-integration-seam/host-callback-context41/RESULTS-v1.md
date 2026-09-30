# Portable result

First frozen strict C++11 ASan/UBSan std::thread gate passed. Named scenarios: two simultaneously active call threads retain distinct origins; a separate background thread stays unsolicited; invalid/mismatched snapshots do not mutate output; nested and foreign-session entry refuse without replacing outer context; four invalid origin-field cases refuse; zero lease is accepted; exception unwind clears context. No fixed aggregate assertion-count oracle.

Source SHA2568e5e66955b713f4a535333a57744ef85b8daa27cb37d79b2c2315af42d8ee679; manifest b5b778dd4cb0c8d4ecf36a96bfa06c4e4f08dcd606d73aa83e1952406cb0a8d3; receipt7ac3730ab1785d078fb67b5d30da417ab7a445dcdb3e9758a13dd99946b34f08.

No VM/native compiler, SDK/vendor/engine or actual callback execution. MSVC TLS spelling is authored but not yet native-compiled. Callback owner must map only validated admission data into Scope, match its own trusted session on snapshot, and supply fresh callback/reverse/intake identities separately. Empty TLS is unsolicited, never EOF. Refusal statuses cannot escape as C++ exceptions through a vendor callback. Stack scope stays on its creating thread; asynchronous callbacks have no scope inheritance. This helper establishes no lifetime pin, callback termination or operational host integration.
