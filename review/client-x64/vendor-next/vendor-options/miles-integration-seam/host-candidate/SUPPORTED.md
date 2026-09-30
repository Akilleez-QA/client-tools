# Advertised compile-only subset

39 operations; no runtime acceptance. All sample operations accept OwnedSample. Only set_sample_volume_levels, set_sample_reverb_levels, set_sample_playback_rate, sample_volume_levels and sample_playback_rate additionally accept parent-guarded BorrowedSample, matching current Audio.cpp calls. Borrowed identities remain distinct; they cannot be independently released or closed.

- `AIL_start_sample`
- `AIL_stop_sample`
- `AIL_end_sample`
- `AIL_start_stream`
- `AIL_active_sample_count`
- `AIL_digital_CPU_percent`
- `AIL_digital_latency`
- `AIL_room_type`
- `AIL_sample_status`
- `AIL_sample_position`
- `AIL_sample_playback_rate`
- `AIL_stream_status`
- `AIL_sample_ms_position`
- `AIL_stream_ms_position`
- `AIL_sample_volume_levels`
- `AIL_sample_reverb_levels`
- `AIL_set_3D_rolloff_factor`
- `AIL_set_room_type`
- `AIL_set_listener_3D_position`
- `AIL_set_listener_3D_velocity_vector`
- `AIL_set_listener_3D_orientation`
- `AIL_set_sample_3D_position`
- `AIL_set_sample_3D_velocity_vector`
- `AIL_set_sample_3D_distances`
- `AIL_set_sample_obstruction`
- `AIL_set_sample_occlusion`
- `AIL_set_sample_volume_levels`
- `AIL_set_sample_reverb_levels`
- `AIL_set_sample_loop_count`
- `AIL_set_sample_ms_position`
- `AIL_set_sample_playback_rate`
- `AIL_set_sample_position`
- `AIL_set_sample_loop_block`
- `AIL_set_stream_loop_block`
- `AIL_set_stream_loop_count`
- `AIL_set_stream_ms_position`
- `AIL_file_error`
- `AIL_get_timer_highest_delay`
- `AIL_serve`

All other frozen opcodes return Unsupported before calling vendor. No exports satisfy a client linker.
