# Native compile-only result

One authorized invocation passed all three object compilations with strict v120 warnings; no link or produced-code execution. AMD64 pipe:20 expected facade definitions and zero AIL imports. x86 Backend anchor:5 actual imports, required subset satisfied (not an exact-count prediction). x86 dispatcher:39 actual imports, exact expected set. All include/header/tool/source identity checks passed.

Receipt SHA256631ccd9ddb7edb87dfbbb64ee85feac49f35f1564599bdb84eb60e9321dddadf. Raw logs, COFF hashes/machines and symbols are in evidence-native-v1. Objects remain private on VM. This establishes compilation and imports only, not original-DLL execution, output behavior, file callbacks, streams or product adoption.

## backend-boundary24/pipe/ClientMilesPipe.cpp

Machine 0x8664; object SHA256e43904e96c89ed35412b96b2630b36c3287d0b9e04435057c6b67f3563d83b88.

No AIL imports.

## alias-native36/host_composition.cpp

Machine 0x14c; object SHA2563bfdce63b8544929f8b6fe3ce95eb09110727eabde775ba4ac066666ff9b25f3.

- `__imp__AIL_allocate_sample_handle@4`
- `__imp__AIL_open_digital_driver@16`
- `__imp__AIL_release_sample_handle@4`
- `__imp__AIL_shutdown@0`
- `__imp__AIL_startup@0`

## host-candidate/host_dispatch.cpp

Machine 0x14c; object SHA256c6f69023fa55fc95b0bf2ba666b38bbc8c9a4d1b255217fab09e5ade1fa5efa2.

- `__imp__AIL_active_sample_count@4`
- `__imp__AIL_digital_CPU_percent@4`
- `__imp__AIL_digital_latency@4`
- `__imp__AIL_end_sample@4`
- `__imp__AIL_file_error@0`
- `__imp__AIL_get_timer_highest_delay@0`
- `__imp__AIL_room_type@4`
- `__imp__AIL_sample_ms_position@12`
- `__imp__AIL_sample_playback_rate@4`
- `__imp__AIL_sample_position@4`
- `__imp__AIL_sample_reverb_levels@12`
- `__imp__AIL_sample_status@4`
- `__imp__AIL_sample_volume_levels@12`
- `__imp__AIL_serve@0`
- `__imp__AIL_set_3D_rolloff_factor@8`
- `__imp__AIL_set_listener_3D_orientation@28`
- `__imp__AIL_set_listener_3D_position@16`
- `__imp__AIL_set_listener_3D_velocity_vector@16`
- `__imp__AIL_set_room_type@8`
- `__imp__AIL_set_sample_3D_distances@16`
- `__imp__AIL_set_sample_3D_position@16`
- `__imp__AIL_set_sample_3D_velocity_vector@16`
- `__imp__AIL_set_sample_loop_block@12`
- `__imp__AIL_set_sample_loop_count@8`
- `__imp__AIL_set_sample_ms_position@8`
- `__imp__AIL_set_sample_obstruction@8`
- `__imp__AIL_set_sample_occlusion@8`
- `__imp__AIL_set_sample_playback_rate@8`
- `__imp__AIL_set_sample_position@8`
- `__imp__AIL_set_sample_reverb_levels@12`
- `__imp__AIL_set_sample_volume_levels@12`
- `__imp__AIL_set_stream_loop_block@12`
- `__imp__AIL_set_stream_loop_count@8`
- `__imp__AIL_set_stream_ms_position@8`
- `__imp__AIL_start_sample@4`
- `__imp__AIL_start_stream@4`
- `__imp__AIL_stop_sample@4`
- `__imp__AIL_stream_ms_position@12`
- `__imp__AIL_stream_status@4`

