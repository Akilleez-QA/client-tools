# Independent review: server host string lengths

Result: no introduced source defect or blocking claim found. One nonblocking receipt wording correction is noted below. This was a read-only source/evidence review with no build, test, runtime, network verification or public action.

Reviewed `review-ready/server-host-string-lengths` at `7dc8ef919449e482817e00017889ec52ee0a75c5` above `09932a32c9949bd40e8e4dbb22e1a7027944eb21`, plus `server-host-string-lengths-body.md`, preparation and receipt. Two commits change two production headers by +5/−5. No tests, build metadata or vendor files are added.

Original `c98f2a6d` and candidate `e889cd3a` share stable patch ID `66979fbc803e4ecf05382838a1eb7a1459f61553`. Original `c03e4a1a` and candidate `7dc8ef91` share `a2e7ec55e9df01286deb68c2dfde433cfb41bbb4`. Their added/removed line sequences also match exactly. The candidate file hashes match the receipt: Misc.h `4331869b95f0760d68746c1702a9f6ec0d0db323d7450d84ba661180c4fd9152`; Tag.h `f918aef2cb7abb3e9f2358d5897e0670e1c8e410723fdbc44efc959ebaf23a93`.

`DuplicateString` keeps the full `strlen + 1` value through allocation and memcpy. `DuplicateStringWithToLower` uses the same host-sized bound and index, retaining the terminator iteration, null behavior and existing character-conversion contract. Tag conversion retains the four iterations, character conversion, left shifts and space padding; only the length/index types change. Existing include context already provides strlen and size_t. No new limit, wire representation, exception policy or allocation strategy is introduced.

The joint base has PR37's renamed `imemmove` helper and size_t forwarding plus PR38's workflow commits. That published helper remains unchanged. This is a suitable retained-history dependency base; tag/duplicate-string arithmetic does not itself call the helper or require unrelated integration source. No network or byte-order descendant was imported.

Both complete headers differ from the compared client files; I independently confirmed those differences and receipt hashes. The immutable client evidence at `56ecc29fc95c62d10241b6cac0d8d9e713961db1`, `review/client-x64/allocator-math-next/RESULTS.md`, reports 4,098 actual-header tags per ABI matching stock and native Debug consumer compilation. The body correctly treats this as supporting historical client evidence, not exact server-header or branch-head qualification. Duplicate helpers follow the already host-sized client implementation; the package does not invent a new server runtime result.

The stated limits cover giant inputs, allocation failures, arbitrary character conversion and full server behavior. Null input to ConvertStringToTag and the signed-char tolower contract are unchanged preconditions, not newly qualified behavior. `git diff --check` is clean; the shared source checkout remained clean and unchanged.

Nonblocking documentation correction: the receipt's final `evidence_scope` field ends “except explicitly recorded timer comparison.” There is no timer in this package. Remove that copied clause; the rest of the field and the PR body accurately state the evidence limit. This does not require source changes or new execution.
