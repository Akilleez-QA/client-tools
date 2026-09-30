#include "ClientMilesPlayback.h"
// Compile-only symbol exercise, NOT a game sequence, test oracle or executable.
// Caller lifetime/binding and policy prerequisites are deliberately not modeled.
void referencePlayback28(ClientMiles::HSAMPLE sample, int32_t signedValue,
                         uint32_t unsignedValue, float value, float *first, float *second,
                         uint32_t *status, uint32_t *position, int32_t *rate) {
    ClientMiles::start_sample(sample);
    ClientMiles::stop_sample(sample);
    *status = ClientMiles::sample_status(sample);
    ClientMiles::set_sample_loop_count(sample, signedValue);
    ClientMiles::set_sample_loop_block(sample, signedValue, signedValue);
    ClientMiles::set_sample_ms_position(sample, signedValue);
    ClientMiles::set_sample_position(sample, unsignedValue);
    *position = ClientMiles::sample_position(sample);
    ClientMiles::set_sample_playback_rate(sample, signedValue);
    *rate = ClientMiles::sample_playback_rate(sample);
    ClientMiles::set_sample_volume_levels(sample, value, value);
    ClientMiles::sample_volume_levels(sample, first, second);
    ClientMiles::set_sample_reverb_levels(sample, value, value);
    ClientMiles::sample_reverb_levels(sample, first, second);
    ClientMiles::set_sample_3D_position(sample, value, value, value);
    ClientMiles::set_sample_3D_velocity_vector(sample, value, value, value);
    ClientMiles::set_sample_3D_distances(sample, value, value, signedValue);
    ClientMiles::set_sample_occlusion(sample, value);
    ClientMiles::set_sample_obstruction(sample, value);
}
