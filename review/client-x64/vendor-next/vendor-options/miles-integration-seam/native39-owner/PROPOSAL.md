# Native39 owner: one-token compatibility successor

Only candidate source change from frozen native38 is removal of the redundant nondependent `typename` before std::aligned_storage in FileRecord. Type, alignment expression, owner logic and tests are unchanged. Native38's first failed compiler output remains intact. The runner differs only in its fresh destination `C:/native39-owner`.

Same six objects/order, actual job (no portable_job), AMD64 v120 Debug flags, /W4 /WX, modern-STL header boundaries, exact required dependency-reference checks, COFF inspection, stop-first-failure and input before/after checks as reviewed38. No compiler is invoked by this preparation. Proposed runner invocation after root authorization only: `C:/ci-dpvs-review/python/python.exe C:/native39-owner/run-native.py --approved-compile-only`.

Input manifest19 entries SHA256: `96dc61ff4a9edd63c7c0597b2a1e6490382e5bbdd34e3e1bf3dc6fcc6c6e9d1a`.
Runner SHA256: `98cc93b04b8826aea577526658df90b313c4156af5c94f33980b7e42e8a42955`.
Owner CPP SHA256: `1dad270fb0f261daa185babf8a6a30781f18a7536b5521bc51ce872f6586e0cb`.
Patch SHA256: `2cd7f370bbc5ace40bdb749138e14d7bb09520aa59fe029e8b91949f64de29d0`.

No other source changes, suppressions, native/runtime execution or product edits. SDK remains absent, objects/PDB remain private if later produced. canonicalServices is still the current mechanism, not final supplied-table integration. A native source pass would not establish host mapping, engine behavior or termination proof.
