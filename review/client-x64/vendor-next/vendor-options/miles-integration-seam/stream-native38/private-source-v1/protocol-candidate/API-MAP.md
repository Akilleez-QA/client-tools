# Exact opcode map (experimental)

No packed SDK structures or callable shim are supplied. Unused fields zero. Signed values use32-bit two's-complement bits; floats use their32-bit bit patterns. `Sample` means OwnedSample unless a row explicitly permits BorrowedSample. Current caller coverage allows borrowed handles only for playback-rate get/set, volume get/set and reverb set; parent-stream lifetime checks still apply. Transport errors are separate from all vendor values, including negative values/null handles. This table describes data representation, not implementation or proven semantic equivalence.

| Opcode | SDK function | Request | Result |
|---:|---|---|---|
|1|`AIL_WAV_info`|resource sealed Buffer; mask bit0 info pointer present (required1 for reviewed Audio call)|S32 return + bytes SoundInfo on success; no host pointers|
|2|`AIL_active_sample_count`|target Driver|S32 return|
|3|`AIL_allocate_sample_handle`|target Driver|nullable OwnedSample handle|
|4|`AIL_close_stream`|target Stream|void; retire stream and borrowed aliases after vendor completion|
|5|`AIL_digital_CPU_percent`|target Driver|S32 return|
|6|`AIL_digital_latency`|target Driver|S32 return|
|7|`AIL_end_sample`|target Sample|void|
|8|`AIL_file_error`|none|S32 return|
|9|`AIL_file_type`|resource sealed Buffer; v0 U32 size <= buffer extent|S32 return|
|10|`AIL_get_preference`|v0 U32 preference ID|signed host32 return, sign-extend into client SINTa|
|11|`AIL_get_timer_highest_delay`|none|U32 return|
|12|`AIL_last_error`|none|copied nullable text|
|13|`AIL_lock`|header lane and current lease for nested acquisition|SDK void; protocol lease in v0/v1 low/high, no fake vendor return|
|14|`AIL_open_digital_driver`|v0 U32 frequency; v1 S32 bits; v2 S32 channels; v3 U32 flags|nullable Driver handle|
|15|`AIL_open_stream`|target Driver; text filename; v0 S32 stream_mem|nullable Stream handle|
|16|`AIL_register_EOS_callback`|target HSAMPLE (OwnedSample in current Audio callers); callback AILSAMPLECB registration token or0|previous callback token (never host trampoline address)|
|17|`AIL_register_stream_callback`|target HSTREAM (Stream only); callback AILSTREAMCB registration token or0|previous callback token (never host trampoline address)|
|18|`AIL_release_sample_handle`|target OwnedSample only|void; retire after callback quiescence|
|19|`AIL_room_type`|target Driver|S32 return|
|20|`AIL_sample_ms_position`|target Sample; mask bit0 total,bit1 current pointers|v0/v1 S32 total/current, only requested outputs|
|21|`AIL_sample_playback_rate`|target Sample (OwnedSample or BorrowedSample)|S32 return|
|22|`AIL_sample_position`|target OwnedSample|U32 return|
|23|`AIL_sample_reverb_levels`|target Sample; mask bits0 dry/1 wet|v0/v1 F32 dry/wet bits|
|24|`AIL_sample_status`|target OwnedSample|U32 return|
|25|`AIL_sample_volume_levels`|target Sample (OwnedSample or BorrowedSample); mask bits0/1|v0/v1 F32 bits (left/right or dry/wet)|
|26|`AIL_serve`|none|void|
|27|`AIL_set_3D_rolloff_factor`|target Driver; v0 F32 bits|void|
|28|`AIL_set_file_callbacks`|v0..7 four uint64 callback-registration tokens (open,close,seek,read)|void|
|29|`AIL_set_listener_3D_orientation`|target Driver; v0..5 F32 face XYZ/up XYZ|void|
|30|`AIL_set_listener_3D_position`|target Driver; v0..2 F32 XYZ|void|
|31|`AIL_set_listener_3D_velocity_vector`|target Driver; v0..2 F32 XYZ|void|
|32|`AIL_set_named_sample_file`|target Sample; resource sealed Buffer; text suffix; v0 U32 file_size; v1 S32 block|S32 vendor return; retain buffer lifetime|
|33|`AIL_set_preference`|v0 U32 ID; v1 signed value checked to host S32|previous signed host32 value|
|34|`AIL_set_redist_directory`|text NUL-terminated exact byte path|copied nullable text|
|35|`AIL_set_room_type`|target Driver; v0 S32 room type|void|
|36|`AIL_set_sample_3D_distances`|target Sample; v0/1 F32 max/min; v2 S32 wet attenuation|void|
|37|`AIL_set_sample_3D_position`|target Sample; v0..2 F32 XYZ|void|
|38|`AIL_set_sample_3D_velocity_vector`|target Sample; v0..2 F32 XYZ|void|
|39|`AIL_set_sample_file`|target Sample; resource sealed Buffer with explicit adapter-known extent; v0 S32 block|S32 vendor return; retain buffer lifetime|
|40|`AIL_set_sample_loop_block`|target Sample; v0/1 S32 start/end offsets|void|
|41|`AIL_set_sample_loop_count`|target Sample; v0 S32|void|
|42|`AIL_set_sample_ms_position`|target Sample; v0 S32|void|
|43|`AIL_set_sample_obstruction`|target Sample; v0 F32 bits|void|
|44|`AIL_set_sample_occlusion`|target Sample; v0 F32 bits|void|
|45|`AIL_set_sample_playback_rate`|target Sample (OwnedSample or BorrowedSample); v0 S32|void|
|46|`AIL_set_sample_position`|target Sample; v0 U32 bytes|void|
|47|`AIL_set_sample_reverb_levels`|target Sample (OwnedSample or BorrowedSample); v0/1 F32 dry/wet|void|
|48|`AIL_set_sample_volume_levels`|target Sample (OwnedSample or BorrowedSample); v0/1 F32 left/right or dry/wet|void|
|49|`AIL_set_stream_loop_block`|target Stream; v0/1 S32 start/end offsets|void|
|50|`AIL_set_stream_loop_count`|target Stream; v0 S32|void|
|51|`AIL_set_stream_ms_position`|target Stream; v0 S32|void|
|52|`AIL_shutdown`|none|void|
|53|`AIL_speaker_configuration`|target Driver; mask bits0 physical,1 logical,2 falloff,3 channels; bit4 vector result requested|v0/1 S32 channels,v2 F32 falloff,v3 S32 spec; nullable bytes vector array only with established count contract|
|54|`AIL_start_sample`|target Sample|void|
|55|`AIL_start_stream`|target Stream|void|
|56|`AIL_startup`|none|S32 return|
|57|`AIL_stop_sample`|target Sample|void|
|58|`AIL_stream_ms_position`|target Stream; mask bit0 total,bit1 current pointers|v0/v1 S32 total/current|
|59|`AIL_stream_sample_handle`|target Stream|stable nullable BorrowedSample tied to stream|
|60|`AIL_stream_status`|target Stream|S32 return|
|61|`AIL_unlock`|header owning lane and matching lease|SDK void; release admission only after actual unlock|

Output masks preserve caller pointer presence; they are not evidence that every SDK pointer may legally be null. Native header types contain no nullability annotations. The reviewed WAV_info caller provides a valid info object; speaker_configuration explicitly passes three null outputs and one valid channel-spec output. Other getters must forward their actual presence pattern and never omit a required output to reduce traffic. Any unused result words stay protocol-zero, not invented SDK output values.

Callback tokens are typed by registration opcode: EOS invokes void AILCALLBACK(HSAMPLE), stream invokes void AILCALLBACK(HSTREAM). Registration results return the previous function pointer identity via local token mapping, not a vendor scalar success code. File callbacks use open U32(MSS_FILE const*,UINTa*), close void(UINTa), seek S32(UINTa,S32,U32), read U32(UINTa,void*,U32). UINTa is pointer-sized locally; protocol File handles replace it with checked registry translation.

## Private protocol version2 pair topology

For opcodes20,23,25,58 only, output_mask value4 means both output pointers are identical. It is legal only with lowbits3: valid masks0,1,2,3,7. Mask7 passes the same host-local pointer to both actual SDK arguments and duplicates its final raw bits into result v0/v1. Clients require identical result words before copyout. Other opcode masks retain their existing meanings. Version1 peers fail the existing exact header-version check; no fallback. This does not change struct sizes or public Miles declarations.

For the client-only stream-proxy37 composition, successful opcode59 replies (including null alias) echo validated parent Stream kind/slot/generation in value0/1/2. Client requires exact requested-parent match before publishing or reusing its cached alias. Host open/close/alias implementation and file integration are not provided by this composition.
