"""Read-only reproducible partition; no provider implementations or SDK changes."""
import json,hashlib,re
from pathlib import Path
base=Path(__file__).resolve().parent
root=Path('/home/akilleez/Work/swg-source/client-build-next')
prior=json.loads((base.parent.parent/'audio-next/miles-live-source-inventory.json').read_text())
groups={
'scalar_commands':'''startup shutdown lock unlock serve set_3D_rolloff_factor set_listener_3D_orientation set_listener_3D_position set_listener_3D_velocity_vector set_room_type set_sample_3D_distances set_sample_3D_position set_sample_3D_velocity_vector set_sample_loop_block set_sample_loop_count set_sample_ms_position set_sample_obstruction set_sample_occlusion set_sample_playback_rate set_sample_position set_sample_reverb_levels set_sample_volume_levels set_stream_loop_block set_stream_loop_count set_stream_ms_position start_sample start_stream stop_sample end_sample'''.split(),
'scalar_getters':'''active_sample_count digital_CPU_percent digital_latency file_error get_preference get_timer_highest_delay room_type sample_ms_position sample_playback_rate sample_position sample_reverb_levels sample_status sample_volume_levels stream_ms_position stream_status'''.split(),
'memory_transfer':'''WAV_info file_type set_named_sample_file set_sample_file'''.split(),
'callback_registration':'''register_EOS_callback register_stream_callback set_file_callbacks'''.split(),
'handle_lifecycle_alias':'''allocate_sample_handle release_sample_handle open_digital_driver open_stream close_stream stream_sample_handle'''.split(),
'pointer_return_or_sized_scalar':'''last_error set_redist_directory speaker_configuration set_preference'''.split(),
'header_macro': ['MSS_version']}
lookup={ 'AIL_'+api:group for group,apis in groups.items() for api in apis }
assert set(lookup)==set(prior['sites']), (set(prior['sites'])-set(lookup),set(lookup)-set(prior['sites']))
rows=[]
for api in sorted(lookup):
 locations=[]
 for file in prior['files']:
  text=(root/file).read_text();locations += [{'file':file,'line':i,'text':line.strip()} for i,line in enumerate(text.splitlines(),1) if re.search(r'\b'+api+r'\s*\(',line)]
 rows.append({'api':api,'primary_group':lookup[api],'current_lexical_locations':locations})
result={'scope':'Prior reviewed 62-name inventory rebased to current lexical source locations; compile/link reachability remains separately established. Categories overlap semantically. No new liveness inference from comments or config guards.', 'source_hashes':{file:hashlib.sha256((root/file).read_bytes()).hexdigest() for file in prior['files']},'groups':{k:len(v) for k,v in groups.items()},'rows':rows}
(base/'api-partition.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['# Miles source seam partition','',result['scope'],'','| API | Primary partition | Current source locations |','|---|---|---|']
for row in rows:
 refs=', '.join(f"{Path(p['file']).name}:{p['line']}" for p in row['current_lexical_locations'])
 lines.append(f"| `{row['api']}` | {row['primary_group']} | {refs} |")
(base/'API-PARTITION.md').write_text('\n'.join(lines)+'\n')
print(result['groups'])
