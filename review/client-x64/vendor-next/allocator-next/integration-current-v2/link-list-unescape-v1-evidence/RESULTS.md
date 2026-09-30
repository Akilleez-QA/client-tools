# Preserve individual native linker dependency tokens

The actual a21af1630 x64 Release and Debug build reached Link but failed LNK1181 opening `.obj`. Each filter property function returned an escaped semicolon list. Plain metadata logging flattened that distinction; earlier manual diagnostic response files bypassed it. Those earlier checks did not prove production task tokenization.

Candidate wraps each existing String.Replace expression in MSBuild::Unescape, in client-runtime-deps.props and parser-deps.props. No input names, removals, order or provider changes. Official documentation explicitly says property-function return strings escape special characters and recommends Unescape when project-literal interpretation is intended: https://learn.microsoft.com/en-us/visualstudio/msbuild/property-functions

16 actual-project native metadata runs pass. x64 SwgClient Release changes 3 aggregate tokens to153 individual tokens; Debug3 to231. Flattened dependency names/order are exactly equal. Both Win32 configurations and all4 Direct3d9 configurations have identical token lists.

Actual native v120 Link task on isolated project/props copies with genuine a21 compiled inputs: baseline fails LNK1181; candidate reaches LNK1120 with61 Miles imports. No command-line list flattening is used in this check: AdditionalDependencies goes directly from actual project metadata to the Link task. This is a custom isolated Link target, not yet the full product Link target.

Controls: omitting actual PCRE provider adds pcre_malloc/free unresolved (63total); supplying real Win32 parser archives instead of x64 adds the15 PCRE/XML imports (76total). All exit1. Wrong-width archives are not selected for undecorated x64 symbols, so this control fails via unresolved symbols rather than LNK1112. No invalid image is run.

Production matrix remains immutable a21 while Win32 tests finish. Full current-head build after this two-line repair is required before claiming integration complete.
