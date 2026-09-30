#include "ClientMilesPlayback.h"
#include <Mss.h>
#include <type_traits>
#if !defined(_WIN64) || _MSC_VER != 1800
#error Requires actual v120 x64 and the pinned private Miles 7.2a header.
#endif
static_assert(std::is_same<uint32_t, U32>::value, "exact unsigned native scalar");
static_assert(std::is_same<int32_t, S32>::value, "exact signed native scalar");
static_assert(std::is_same<float, F32>::value, "exact native floating point");
static_assert(std::is_same<decltype(&::AIL_start_sample), void (AILCALL *)(::HSAMPLE)>::value, "actual start_sample declaration");
static_assert(std::is_same<decltype(&ClientMiles::start_sample), void (*)(ClientMiles::HSAMPLE)>::value, "facade start_sample shape");
static_assert(std::is_same<decltype(&::AIL_stop_sample), void (AILCALL *)(::HSAMPLE)>::value, "actual stop_sample declaration");
static_assert(std::is_same<decltype(&ClientMiles::stop_sample), void (*)(ClientMiles::HSAMPLE)>::value, "facade stop_sample shape");
static_assert(std::is_same<decltype(&::AIL_sample_status), U32 (AILCALL *)(::HSAMPLE)>::value, "actual sample_status declaration");
static_assert(std::is_same<decltype(&ClientMiles::sample_status), U32 (*)(ClientMiles::HSAMPLE)>::value, "facade sample_status shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_loop_count), void (AILCALL *)(::HSAMPLE, S32)>::value, "actual set_sample_loop_count declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_loop_count), void (*)(ClientMiles::HSAMPLE, S32)>::value, "facade set_sample_loop_count shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_loop_block), void (AILCALL *)(::HSAMPLE, S32, S32)>::value, "actual set_sample_loop_block declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_loop_block), void (*)(ClientMiles::HSAMPLE, S32, S32)>::value, "facade set_sample_loop_block shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_ms_position), void (AILCALL *)(::HSAMPLE, S32)>::value, "actual set_sample_ms_position declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_ms_position), void (*)(ClientMiles::HSAMPLE, S32)>::value, "facade set_sample_ms_position shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_position), void (AILCALL *)(::HSAMPLE, U32)>::value, "actual set_sample_position declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_position), void (*)(ClientMiles::HSAMPLE, U32)>::value, "facade set_sample_position shape");
static_assert(std::is_same<decltype(&::AIL_sample_position), U32 (AILCALL *)(::HSAMPLE)>::value, "actual sample_position declaration");
static_assert(std::is_same<decltype(&ClientMiles::sample_position), U32 (*)(ClientMiles::HSAMPLE)>::value, "facade sample_position shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_playback_rate), void (AILCALL *)(::HSAMPLE, S32)>::value, "actual set_sample_playback_rate declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_playback_rate), void (*)(ClientMiles::HSAMPLE, S32)>::value, "facade set_sample_playback_rate shape");
static_assert(std::is_same<decltype(&::AIL_sample_playback_rate), S32 (AILCALL *)(::HSAMPLE)>::value, "actual sample_playback_rate declaration");
static_assert(std::is_same<decltype(&ClientMiles::sample_playback_rate), S32 (*)(ClientMiles::HSAMPLE)>::value, "facade sample_playback_rate shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_volume_levels), void (AILCALL *)(::HSAMPLE, F32, F32)>::value, "actual set_sample_volume_levels declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_volume_levels), void (*)(ClientMiles::HSAMPLE, F32, F32)>::value, "facade set_sample_volume_levels shape");
static_assert(std::is_same<decltype(&::AIL_sample_volume_levels), void (AILCALL *)(::HSAMPLE, F32 *, F32 *)>::value, "actual sample_volume_levels declaration");
static_assert(std::is_same<decltype(&ClientMiles::sample_volume_levels), void (*)(ClientMiles::HSAMPLE, F32 *, F32 *)>::value, "facade sample_volume_levels shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_reverb_levels), void (AILCALL *)(::HSAMPLE, F32, F32)>::value, "actual set_sample_reverb_levels declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_reverb_levels), void (*)(ClientMiles::HSAMPLE, F32, F32)>::value, "facade set_sample_reverb_levels shape");
static_assert(std::is_same<decltype(&::AIL_sample_reverb_levels), void (AILCALL *)(::HSAMPLE, F32 *, F32 *)>::value, "actual sample_reverb_levels declaration");
static_assert(std::is_same<decltype(&ClientMiles::sample_reverb_levels), void (*)(ClientMiles::HSAMPLE, F32 *, F32 *)>::value, "facade sample_reverb_levels shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_3D_position), void (AILCALL *)(::HSAMPLE, F32, F32, F32)>::value, "actual set_sample_3D_position declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_position), void (*)(ClientMiles::HSAMPLE, F32, F32, F32)>::value, "facade set_sample_3D_position shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_3D_velocity_vector), void (AILCALL *)(::HSAMPLE, F32, F32, F32)>::value, "actual set_sample_3D_velocity_vector declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_velocity_vector), void (*)(ClientMiles::HSAMPLE, F32, F32, F32)>::value, "facade set_sample_3D_velocity_vector shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_3D_distances), void (AILCALL *)(::HSAMPLE, F32, F32, S32)>::value, "actual set_sample_3D_distances declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_distances), void (*)(ClientMiles::HSAMPLE, F32, F32, S32)>::value, "facade set_sample_3D_distances shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_occlusion), void (AILCALL *)(::HSAMPLE, F32)>::value, "actual set_sample_occlusion declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_occlusion), void (*)(ClientMiles::HSAMPLE, F32)>::value, "facade set_sample_occlusion shape");
static_assert(std::is_same<decltype(&::AIL_set_sample_obstruction), void (AILCALL *)(::HSAMPLE, F32)>::value, "actual set_sample_obstruction declaration");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_obstruction), void (*)(ClientMiles::HSAMPLE, F32)>::value, "facade set_sample_obstruction shape");

namespace ClientMiles {
void start_sample(HSAMPLE sample) {
    ::AIL_start_sample(reinterpret_cast<::HSAMPLE>(sample));
}
void stop_sample(HSAMPLE sample) {
    ::AIL_stop_sample(reinterpret_cast<::HSAMPLE>(sample));
}
uint32_t sample_status(HSAMPLE sample) {
    return ::AIL_sample_status(reinterpret_cast<::HSAMPLE>(sample));
}
void set_sample_loop_count(HSAMPLE sample, int32_t count) {
    ::AIL_set_sample_loop_count(reinterpret_cast<::HSAMPLE>(sample), count);
}
void set_sample_loop_block(HSAMPLE sample, int32_t startByte, int32_t endByte) {
    ::AIL_set_sample_loop_block(reinterpret_cast<::HSAMPLE>(sample), startByte, endByte);
}
void set_sample_ms_position(HSAMPLE sample, int32_t milliseconds) {
    ::AIL_set_sample_ms_position(reinterpret_cast<::HSAMPLE>(sample), milliseconds);
}
void set_sample_position(HSAMPLE sample, uint32_t byteOffset) {
    ::AIL_set_sample_position(reinterpret_cast<::HSAMPLE>(sample), byteOffset);
}
uint32_t sample_position(HSAMPLE sample) {
    return ::AIL_sample_position(reinterpret_cast<::HSAMPLE>(sample));
}
void set_sample_playback_rate(HSAMPLE sample, int32_t rate) {
    ::AIL_set_sample_playback_rate(reinterpret_cast<::HSAMPLE>(sample), rate);
}
int32_t sample_playback_rate(HSAMPLE sample) {
    return ::AIL_sample_playback_rate(reinterpret_cast<::HSAMPLE>(sample));
}
void set_sample_volume_levels(HSAMPLE sample, float left, float right) {
    ::AIL_set_sample_volume_levels(reinterpret_cast<::HSAMPLE>(sample), left, right);
}
void sample_volume_levels(HSAMPLE sample, float * left, float * right) {
    ::AIL_sample_volume_levels(reinterpret_cast<::HSAMPLE>(sample), left, right);
}
void set_sample_reverb_levels(HSAMPLE sample, float dry, float wet) {
    ::AIL_set_sample_reverb_levels(reinterpret_cast<::HSAMPLE>(sample), dry, wet);
}
void sample_reverb_levels(HSAMPLE sample, float * dry, float * wet) {
    ::AIL_sample_reverb_levels(reinterpret_cast<::HSAMPLE>(sample), dry, wet);
}
void set_sample_3D_position(HSAMPLE sample, float x, float y, float z) {
    ::AIL_set_sample_3D_position(reinterpret_cast<::HSAMPLE>(sample), x, y, z);
}
void set_sample_3D_velocity_vector(HSAMPLE sample, float xPerMs, float yPerMs, float zPerMs) {
    ::AIL_set_sample_3D_velocity_vector(reinterpret_cast<::HSAMPLE>(sample), xPerMs, yPerMs, zPerMs);
}
void set_sample_3D_distances(HSAMPLE sample, float maximum, float minimum, int32_t autoWetAttenuation) {
    ::AIL_set_sample_3D_distances(reinterpret_cast<::HSAMPLE>(sample), maximum, minimum, autoWetAttenuation);
}
void set_sample_occlusion(HSAMPLE sample, float value) {
    ::AIL_set_sample_occlusion(reinterpret_cast<::HSAMPLE>(sample), value);
}
void set_sample_obstruction(HSAMPLE sample, float value) {
    ::AIL_set_sample_obstruction(reinterpret_cast<::HSAMPLE>(sample), value);
}
}
