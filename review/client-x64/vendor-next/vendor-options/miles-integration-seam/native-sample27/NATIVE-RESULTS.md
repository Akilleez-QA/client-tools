# Native sample27 object gate

The single parent-authorized v120 AMD64 gate passed on its first attempt in C:/native-sample27. Header/type discovery, object compilation and symbol inspection all exited 0. All native scalar/signature assertions compiled against the actual pinned private 7.2a header. No link, executable, import library, vendor loading or engine/runtime work occurred.

The receipt is `evidence-native-v1/receipt.json`, SHA256 6bd45d43d5d6e4a7430eafa1d360db2c3bd7d0caa40db908eb6452c01f10ca1c. It records unchanged before/after identities for 6 source files, 84 transitive headers including Mss.h SHA 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e, 45 tool files and 5 Python builders. Exact native commands, environment selection and diagnostics are retained beside the receipt. The fetched text receipt matches the externally captured pin.

| Object retained privately on VM | COFF machine | Immediate SHA256 |
|---|---|---|
| native_sample27.obj | 0x8664 | 6abe1b3641b0917ae543f2d09defc4ba83f59ff6f2d7a0fbda2bbf22f8fea9b3 |
| sample_time.obj | 0x8664 | a2206d2920eab39aab71fb67e8646ba7244b403981b6a40dfe416bfe265127f6 |
| portable_contract.obj | 0x8664 | 4a0060bbdd300af19a66daace0c8ca4e9cd101810954c68efb2b8e75c683d7eb |

`native_sample27.obj` has exactly these five unresolved vendor imports: AIL_allocate_sample_handle, AIL_set_named_sample_file, AIL_sample_ms_position, AIL_end_sample and AIL_release_sample_handle. No replacement definitions were supplied. The private output directory contains no .exe, .dll or .lib.

All 15 source-manifest members and all 23 original preparation-packet members were rechecked unchanged after the gate. The source archive remains 34dd35b74995f1166d6b4ba68391feaa53e8e367812e0ea7b1a7aab23351eb82; manifest remains ec62d406a40293fc10bc9420707a78d5379b771d9d9289d9298f57a6bc7afdee. The original RESULTS.md and packet-v1.tar are historical preparation evidence, preserved rather than rewritten. The new text packet uses packet-manifest-v2.json: a flat packet-relative path-to-{bytes,sha256} map rooted at native-sample27, with no binary objects, SDK bodies or nested archives.

Delivery state: built to objects. Outcome: passed for the prepared actual-header compile/type/import gate. This supports the five-operation native source shape with explicitly adapted opaque handles. It does not establish a linked Miles64 runtime, legal nullable-output combinations at runtime, image or callback lifetime behavior, failure recovery, playback, pipe support or whole-client fidelity. The example's normal failed-bind release is source-visible, not runtime-tested. Parent controls any next gate.
