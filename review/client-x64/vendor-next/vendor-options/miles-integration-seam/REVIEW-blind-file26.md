# Blind source review: file-channel26

**Verdict:** no confirmed must-fix defect found in the bounded private value adapter under its stated trusted, serialized executor and external file-owner preconditions. This is not approval to integrate or execute against the engine.

**Fresh scores:** bounded source quality **8.8/10**; production integration readiness **3/10**. The first reflects clear validation, ownership and side-effect separation plus portable evidence. The second reflects missing real admission/TLS/serialization and publication/retirement proof, which this candidate explicitly leaves external. These are separate assessments, not an average.

Reviewed 2026-09-30 by fresh reviewer agent `/root/astra_file26_blind`, independently from the source author. No worker RESULTS or peer review contents were consulted. Reviewer and author share an OpenAI GPT model family; this is not human or different-family independence.

## Frozen identity and scope

Manifest SHA-256: `b064bdbf619920c045f1e5f1b3a9327d3141b76e6d886d651566dc1fd9931425`. All 16 manifest entries matched before and after review.

| Raw source | SHA-256 |
| --- | --- |
| file_channel.h | `58b4c91c09207e2c83c0700c7b85056370c1694aaca5f0ae7346eb0c53076fde` |
| file_channel.cpp | `0c5253d7f2a3a7b06ba54af756f170eca6c5f3b84fbbdce952a5700de6a64e27` |
| canonical_services.cpp | `3b9777f73e1940df24da9e319a4eb1a635d94634904ff66dd2e3726433218430` |
| channel_test.cpp | `b107ca407a6a468a6171400d3d0bdd7afb31551ca7aacbdb8b586f0fd256a91c` |
| seam20 ClientAudioFileCallbacks.h | `d116186a05fc44cc4809231ff114aa526514edb6155e40e70edd6a147769a9b0` |

Read these raw sources first, then CONTRACT.md, the generic codec/schema dependencies and the check script. No product or frozen source was changed. Builds and new tests are confined to `review-scratch-file26/blind-astra/`.

## Findings and evidence

No actionable correctness finding survived review within the declared boundary:

- **Malformed fields:** `file_channel.cpp:62–103,222–248` validates association, opcode-specific fields, count limits and reply byte/count equality. The codec additionally rejects reserved bits, malformed handles, noncanonical empty spans, truncation and trailing data. Added tests mutated unused request scalars, forbidden request/reply fields and every truncation length for representative frames; rejection preserved output.
- **Key zero and signedness:** `147–155,200–207` bases open success on callbackResult, never local key truthiness, and publishes only an externally supplied File identity. Failed-open key bits stay diagnostic. Added tests exercised signed seek minimum, maximum, -1 and zero with all three origins; callback input and return bits were preserved.
- **Storage, exceptions and side effects:** `117–175` copies input and allocates staging before service entry. One admitted Invocation cannot call twice, including reentry. Read exceptions retain an unknown outcome rather than EOF. Added throw tests for close, seek and read confirmed one service entry and rejected ordinary reply encoding. Existing tests cover throwing open and post-open encoding allocation failure. Added decode allocation failure left the old OwnedReply unchanged. Successful maximum-size read encoded to exactly MaxFrameBytes and decoded with owned bytes.
- **Pins and copyRead:** the Invocation retains binding and context until destruction; its documented caller-retention requirement is necessary. No automatic retry, close or cleanup defeats external ownership. `261–270` validates null file identity, actual/requested count, exact owned byte size, destination capacity and null destination before writing; short reads preserve the destination tail and EOF writes nothing. As with ordinary C++ buffer APIs, actual destination validity is a caller obligation.

Portable GCC C++11 build with `-Wall -Wextra -Werror -fsanitize=address,undefined` passed **1,039 assertions**: 157 existing plus 882 added. Logs, test source, compiler identity and post-review hash check are in `review-scratch-file26/blind-astra/`. The canonical adapter compiled separately; `nm -C -u` showed the four expected unresolved seam20 functions. It was not linked to or executed against their real implementations.

## Remaining acceptance work and limits

Keep production integration blocked until the existing engine executor establishes TLS/lifetime and serialization with all original callbacks, and the external file owner proves publication/retirement behavior for successful unpublished opens, uncertain throws, disconnects and close. These are documented preconditions, not newly assigned adapter responsibilities. This review found no adapter path that defeats them when honored.

The test role label and Coordinator script do not prove an engine executor or complete cancellation system. No vendor library, VM, engine runtime, real file callback, native Windows compiler, race test or global fault-injection campaign was used. Portable success establishes value-path behavior only. Before widening the boundary, retain the added malformed-field, extreme-seek, maximum-read and non-open exception cases as regression evidence; no architecture remake is recommended.
