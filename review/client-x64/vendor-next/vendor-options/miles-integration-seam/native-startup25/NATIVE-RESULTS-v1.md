# Authorized native compile-only result v1

Passed on the first invocation at C:/native-startup25 using real v120 amd64. Header discovery and /c compilation both exited zero with warnings-as-errors. Four objects were produced: pinned native24 adapter, new native25 adapter, the same install-order source used in portable checks, and the portable declaration contract. All COFF machine values are 0x8664. Source/builder/header/tool identity checks passed unchanged.

The four exact file callback typedef comparisons against private Miles 7.2a compiled. The new adapter object has unresolved imports for all eight actual SDK operations: AIL_set_file_callbacks, AIL_set_listener_3D_position, AIL_set_listener_3D_velocity_vector, AIL_set_listener_3D_orientation, AIL_set_3D_rolloff_factor, AIL_serve, AIL_room_type and AIL_set_room_type. Thus these are direct references to real SDK operations, not local success stubs.

Receipt SHA-256: 5c6ac990057779494edd7b97e188ba6c3bd229046cd59af14d4760cd7dde0d3e. Frozen source manifest: 997c2b72117c3b2f64654bb0fd0de7caee4617ab8bd5fd4097c150af8098b597. Frozen source archive: 7090ee3e90f6af53e4e49125d195cd90a271d8e7961c3190a56b94952dcdd9ce.

No link, import-library generation, produced executable, vendor DLL load, engine execution or game launch occurred. Object files remain private on the VM and are excluded from the shareable packet. The private SDK/header/tool contents are also excluded; receipts contain only their identities and include paths. Portable object files are excluded too.

This establishes source/type/object compatibility with the possessed header and compiler only. It does not establish successful native64 runtime linking, audio fidelity, callback execution context, buffer lifetime, install-policy equivalence or partial-startup/shutdown safety. The source excerpt still deliberately omits engine policy/work. Frozen24 and product were not edited. The pre-authorization RESULTS.md remains frozen; this file supplies the subsequent result.
