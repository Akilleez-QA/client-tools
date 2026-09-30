#ifndef CLIENT_MILES_PLAYBACK28_H
#define CLIENT_MILES_PLAYBACK28_H
#include "../native-sample27/ClientMilesSample.h"
namespace ClientMiles {
// These controls use the common HSAMPLE type. Owned samples remain valid until
// release. Borrowed stream samples remain valid only while their parent is live.
// Borrowed use in this subset: set_sample_volume_levels, sample_volume_levels,
// set_sample_reverb_levels, set_sample_playback_rate and sample_playback_rate.
// Other declarations here require owned samples; no callback/ownership transfer.
void start_sample(HSAMPLE sample);
void stop_sample(HSAMPLE sample);
uint32_t sample_status(HSAMPLE sample);
void set_sample_loop_count(HSAMPLE sample, int32_t count);
void set_sample_loop_block(HSAMPLE sample, int32_t startByte, int32_t endByte);
void set_sample_ms_position(HSAMPLE sample, int32_t milliseconds);
void set_sample_position(HSAMPLE sample, uint32_t byteOffset);
uint32_t sample_position(HSAMPLE sample);
void set_sample_playback_rate(HSAMPLE sample, int32_t rate);
int32_t sample_playback_rate(HSAMPLE sample);
void set_sample_volume_levels(HSAMPLE sample, float left, float right);
void sample_volume_levels(HSAMPLE sample, float * left, float * right);
void set_sample_reverb_levels(HSAMPLE sample, float dry, float wet);
void sample_reverb_levels(HSAMPLE sample, float * dry, float * wet);
void set_sample_3D_position(HSAMPLE sample, float x, float y, float z);
void set_sample_3D_velocity_vector(HSAMPLE sample, float xPerMs, float yPerMs, float zPerMs);
void set_sample_3D_distances(HSAMPLE sample, float maximum, float minimum, int32_t autoWetAttenuation);
void set_sample_occlusion(HSAMPLE sample, float value);
void set_sample_obstruction(HSAMPLE sample, float value);
// Byte positions/loop offsets and millisecond positions remain distinct SDK units.
// Getter output pointers pass through unchanged, including null; this facade adds
// no pointer-validity guarantees beyond the actual SDK contract. Stop, end and
// release stay separate. No clamping, scheduling, range narrowing or replay.
}
#endif
