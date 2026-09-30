# Source/portable result

First portable invocation passed1209 checks under C++11 strict warnings and ASan/UBSan. No SDK, VM, vendor or engine execution. Source frozen before tests; old34 unchanged.

Source SHA2565f4821e6f3d7fd011c3926c0ff638ddefa7c66a88073374b014f8bc4bde43629; manifest71e13b03df1ddd336ff243ed168717ca78df042a87b483b1dc40cc0df98fbd87; portable receipt359039f9d0155f324a7ead23048c4201025c19310ae910c4ab26ade2b73c8e9f.

Tests cover actual framed client traffic, shared host helper address topology and validation, all19 controls, three implemented client pair getters, null output masks, bitwise negative-zero/NaN patterns, aliased outputs, inconsistent alias replies rejected before mutation, terminal uncertainty and old-version rejection. They do not execute actual host_dispatch or establish SDK nullability/preconditions/getter behavior. Native compilation is proposed separately in alias-native36 and has not run.

This makes alias topology explicit rather than relying on SDK assignment order. It is not evidence that34 produced wrong runtime output: parent reports separate static-DLL analysis consistent with34's copyout order, subject to parent verification. No initial-value serialization, sample binding or playback introduced.
