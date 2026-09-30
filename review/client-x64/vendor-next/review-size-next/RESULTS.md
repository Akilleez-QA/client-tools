# Independent C/C++ source-only size comparison

Same base94945103; existing local refs only. git diff --numstat under src/, numeric rows with case-insensitive extensions .c/.cc/.cpp/.cxx/.h/.hh/.hpp/.hxx/.inl. Excludes test/build tooling outside src, XML, binaries and other extensions.

| Head | Files | Added | Deleted | Changed |
|---|---:|---:|---:|---:|
| a21af1630 |105|1396|520|1916|
| PR21 46f6003ac |1564|422164|7012|429176|

PR21 categories: all third-party source880files,+328323/-334; JUCE8.0.14 alone830files,+327632/-0. New Direct3d11 implementation89files,+64156/-0, including the explicitly GENERATED Direct3d11_EmbeddedShaderCorpus.cpp39732addedlines. Excluding all thirdparty leaves684files,+93841/-6678, still includes an entirely new renderer and generated shader data. These numbers are not equal-scope implementation comparisons or a completeness measure. No equivalent-work ratio is justified.
