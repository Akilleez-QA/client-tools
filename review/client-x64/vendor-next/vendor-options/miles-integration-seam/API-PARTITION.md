# Miles source seam partition

Prior reviewed 62-name inventory rebased to current lexical source locations; compile/link reachability remains separately established. Categories overlap semantically. No new liveness inference from comments or config guards.

| API | Primary partition | Current source locations |
|---|---|---|
| `AIL_MSS_version` | header_macro | Audio.cpp:2469 |
| `AIL_WAV_info` | memory_transfer | Audio.cpp:3710 |
| `AIL_active_sample_count` | scalar_getters | Audio.cpp:681, Audio.cpp:683, Audio.cpp:2900, Audio.cpp:3005 |
| `AIL_allocate_sample_handle` | handle_lifecycle_alias | Audio.cpp:630, Audio.cpp:660, Audio.cpp:4437, Audio.cpp:5334, Audio.cpp:5354 |
| `AIL_close_stream` | handle_lifecycle_alias | Audio.cpp:3367 |
| `AIL_digital_CPU_percent` | scalar_getters | Audio.cpp:3526 |
| `AIL_digital_latency` | scalar_getters | Audio.cpp:3539 |
| `AIL_end_sample` | scalar_commands | Audio.cpp:3357, Audio.cpp:3362, Audio.cpp:4454, Audio.cpp:5373, Audio.cpp:5383 |
| `AIL_file_error` | scalar_getters | Audio.cpp:4547 |
| `AIL_file_type` | memory_transfer | Audio.cpp:2546 |
| `AIL_get_preference` | scalar_getters | Audio.cpp:1297 |
| `AIL_get_timer_highest_delay` | scalar_getters | Audio.cpp:1943 |
| `AIL_last_error` | pointer_return_or_sized_scalar | Audio.cpp:1306, Audio.cpp:1313, Audio.cpp:2899, Audio.cpp:3004 |
| `AIL_lock` | scalar_commands | Audio.cpp:4922 |
| `AIL_open_digital_driver` | handle_lifecycle_alias | Audio.cpp:1301, Audio.cpp:1307 |
| `AIL_open_stream` | handle_lifecycle_alias | Audio.cpp:605 |
| `AIL_register_EOS_callback` | callback_registration | Audio.cpp:2878, Audio.cpp:2960 |
| `AIL_register_stream_callback` | callback_registration | Audio.cpp:3072 |
| `AIL_release_sample_handle` | handle_lifecycle_alias | Audio.cpp:3394, Audio.cpp:3403, Audio.cpp:4455 |
| `AIL_room_type` | scalar_getters | Audio.cpp:3826 |
| `AIL_sample_ms_position` | scalar_getters | Audio.cpp:4251, Audio.cpp:4303, Audio.cpp:4349, Audio.cpp:4453 |
| `AIL_sample_playback_rate` | scalar_getters | Audio.cpp:3326, Audio.cpp:3330, Audio.cpp:3334 |
| `AIL_sample_position` | scalar_getters | Audio.cpp:4267, Audio.cpp:4314 |
| `AIL_sample_reverb_levels` | scalar_getters | Audio.cpp:3928 |
| `AIL_sample_status` | scalar_getters | Audio.cpp:2706, Audio.cpp:2711 |
| `AIL_sample_volume_levels` | scalar_getters | Audio.cpp:2892, Audio.cpp:2995, Audio.cpp:3287, Audio.cpp:3296, Audio.cpp:3305 |
| `AIL_serve` | scalar_commands | Audio.cpp:2448, Audio.cpp:4958, Audio.cpp:5119, Audio.cpp:5126 |
| `AIL_set_3D_rolloff_factor` | scalar_commands | Audio.cpp:1324 |
| `AIL_set_file_callbacks` | callback_registration | Audio.cpp:1293 |
| `AIL_set_listener_3D_orientation` | scalar_commands | SoundObject3d.cpp:34 |
| `AIL_set_listener_3D_position` | scalar_commands | SoundObject3d.cpp:32 |
| `AIL_set_listener_3D_velocity_vector` | scalar_commands | SoundObject3d.cpp:33 |
| `AIL_set_named_sample_file` | memory_transfer | Audio.cpp:2836, Audio.cpp:4449, Audio.cpp:5338, Audio.cpp:5358 |
| `AIL_set_preference` | pointer_return_or_sized_scalar | Audio.cpp:5118, Audio.cpp:5125 |
| `AIL_set_redist_directory` | pointer_return_or_sized_scalar | Audio.cpp:1285 |
| `AIL_set_room_type` | scalar_commands | Audio.cpp:3788, Audio.cpp:3789, Audio.cpp:3790, Audio.cpp:3791, Audio.cpp:3792, Audio.cpp:3793, Audio.cpp:3794, Audio.cpp:3795, Audio.cpp:3796, Audio.cpp:3797, Audio.cpp:3798, Audio.cpp:3799, Audio.cpp:3800, Audio.cpp:3801, Audio.cpp:3802, Audio.cpp:3803, Audio.cpp:3804, Audio.cpp:3805, Audio.cpp:3806, Audio.cpp:3807, Audio.cpp:3808, Audio.cpp:3809, Audio.cpp:3810, Audio.cpp:3811, Audio.cpp:3812, Audio.cpp:3813 |
| `AIL_set_sample_3D_distances` | scalar_commands | Audio.cpp:2988 |
| `AIL_set_sample_3D_position` | scalar_commands | Audio.cpp:2461, Audio.cpp:2965 |
| `AIL_set_sample_3D_velocity_vector` | scalar_commands | Audio.cpp:2966 |
| `AIL_set_sample_file` | memory_transfer | Audio.cpp:2925 |
| `AIL_set_sample_loop_block` | scalar_commands | Audio.cpp:2851 |
| `AIL_set_sample_loop_count` | scalar_commands | Audio.cpp:2865, Audio.cpp:2873, Audio.cpp:2947, Audio.cpp:2955 |
| `AIL_set_sample_ms_position` | scalar_commands | Audio.cpp:4391 |
| `AIL_set_sample_obstruction` | scalar_commands | Audio.cpp:3144 |
| `AIL_set_sample_occlusion` | scalar_commands | Audio.cpp:3129 |
| `AIL_set_sample_playback_rate` | scalar_commands | Audio.cpp:3244, Audio.cpp:3252, Audio.cpp:3260 |
| `AIL_set_sample_position` | scalar_commands | Audio.cpp:4406 |
| `AIL_set_sample_reverb_levels` | scalar_commands | Audio.cpp:3174, Audio.cpp:3197, Audio.cpp:3212, Audio.cpp:3911 |
| `AIL_set_sample_volume_levels` | scalar_commands | Audio.cpp:3173, Audio.cpp:3196, Audio.cpp:3211, Audio.cpp:5342, Audio.cpp:5362, Audio.cpp:5391, Audio.cpp:5400 |
| `AIL_set_stream_loop_block` | scalar_commands | Audio.cpp:3041 |
| `AIL_set_stream_loop_count` | scalar_commands | Audio.cpp:3059, Audio.cpp:3067 |
| `AIL_set_stream_ms_position` | scalar_commands | Audio.cpp:4421 |
| `AIL_shutdown` | scalar_commands | Audio.cpp:1437 |
| `AIL_speaker_configuration` | pointer_return_or_sized_scalar | Audio.cpp:1326 |
| `AIL_start_sample` | scalar_commands | Audio.cpp:2883, Audio.cpp:2894, Audio.cpp:2992, Audio.cpp:2995, Audio.cpp:4387, Audio.cpp:5344, Audio.cpp:5364 |
| `AIL_start_stream` | scalar_commands | Audio.cpp:3080, Audio.cpp:3083, Audio.cpp:4417 |
| `AIL_startup` | scalar_commands | Audio.cpp:1289 |
| `AIL_stop_sample` | scalar_commands | Audio.cpp:3356, Audio.cpp:3361, Audio.cpp:5372, Audio.cpp:5382 |
| `AIL_stream_ms_position` | scalar_getters | Audio.cpp:4224, Audio.cpp:4282, Audio.cpp:4328, Audio.cpp:4368 |
| `AIL_stream_sample_handle` | handle_lifecycle_alias | Audio.cpp:3211, Audio.cpp:3212, Audio.cpp:3260, Audio.cpp:3305, Audio.cpp:3334 |
| `AIL_stream_status` | scalar_getters | Audio.cpp:2716 |
| `AIL_unlock` | scalar_commands | Audio.cpp:4928 |
