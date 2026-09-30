# Audio preference/count narrowing candidate

One production file: Audio.cpp. Parent approved separate root-cause commit.
DIG_MIXER_CHANNELS is never set by this client. Its vendor SINTa result feeds an
existing int getter, sample-limit min(), diagnostics and SoundEditor. Local SDK
declarations cannot prove its runtime range. Preserve the int API and every
representable value (including negatives), reject outside INT_MIN..INT_MAX using
always-enabled FATAL before casting. On Win32 SINTa is already 32-bit. This does
not establish a working native x64 Miles SDK or vendor runtime.

Three unused debug map-size snapshots now use size_t. The remaining file-map
count is size_t and printed through existing PRIu64/uint64_t conventions.
No archive/header edits, callback lifetime edits, feature changes or SDK substitutes.

Prediction: these specific Audio.cpp warnings disappear on both ABIs. Current
Debug-x64 build is independently blocked by Archive.h:311 size_t narrowing; do not
suppress that warning or describe a failed TU as pass. Native compile of all four
configurations remains pending the separately owned Archive repair. SDK-return
rejection boundary needs diagnostic coverage separate from a claimed SDK call.

## Measured follow-up

Native v120 actual clientAudio project Rebuild passed all four configurations,
including original Debug /WX, with this Audio candidate and separately owned
Archive checked-once string-length candidate. Exact source copies, commands and
logs are in audio-narrowing-v1. Outputs/PCH placed outside frozen matrix.

SDK-header SINTa arithmetic probe passed 4/4 Win32 and 6/6 x64 in both Debug and
Release. Cases: INT_MIN,-1,0,INT_MAX, plus x64 INT_MIN-1 and INT_MAX+1. This is an
arithmetic conversion oracle only: it does not call Miles, substitute Miles,
exercise production Audio::install or observe the real FATAL termination path.
Those boundaries remain explicitly distinct. Both source files restored in the
private integration tree after compile; original product checkout untouched.
