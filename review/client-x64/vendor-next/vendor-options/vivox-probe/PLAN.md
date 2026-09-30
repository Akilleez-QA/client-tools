# Prospective local-only Vivox probe

Prediction: original x86 DLL loads in native v120 Win32 and resolves all52 wrapper imports; string and unissued aux request allocation/destruction succeed through actual SDK declarations. Native x64 cannot load this x86 artifact (expected architecture failure, not backend pass). No vx_issue_request, vx_alloc_sdk_handle, connector, account, service process, device enumeration request, network or credentials. Merely create an unissued request object then destroy it. No product mutation. DLL loading itself is observed as a black-box operation; this probe cannot certify arbitrary vendor internals never attempt background initialization.

Bind exact binary/header/source hashes, dependencies and file version. Missing imports, unsuccessful lifecycle or crash remain failure. Existing service architecture is inspected without executing its EXE. Scope: local loader/ABI seam only, no voice functionality or service compatibility claim.
