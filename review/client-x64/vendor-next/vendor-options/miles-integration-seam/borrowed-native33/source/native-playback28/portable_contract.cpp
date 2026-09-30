#include "ClientMilesPlayback.h"
#include <type_traits>
static_assert(std::is_same<decltype(&ClientMiles::start_sample), void (*)(ClientMiles::HSAMPLE)>::value, "start_sample source shape");
static_assert(std::is_same<decltype(&ClientMiles::stop_sample), void (*)(ClientMiles::HSAMPLE)>::value, "stop_sample source shape");
static_assert(std::is_same<decltype(&ClientMiles::sample_status), uint32_t (*)(ClientMiles::HSAMPLE)>::value, "sample_status source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_loop_count), void (*)(ClientMiles::HSAMPLE, int32_t)>::value, "set_sample_loop_count source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_loop_block), void (*)(ClientMiles::HSAMPLE, int32_t, int32_t)>::value, "set_sample_loop_block source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_ms_position), void (*)(ClientMiles::HSAMPLE, int32_t)>::value, "set_sample_ms_position source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_position), void (*)(ClientMiles::HSAMPLE, uint32_t)>::value, "set_sample_position source shape");
static_assert(std::is_same<decltype(&ClientMiles::sample_position), uint32_t (*)(ClientMiles::HSAMPLE)>::value, "sample_position source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_playback_rate), void (*)(ClientMiles::HSAMPLE, int32_t)>::value, "set_sample_playback_rate source shape");
static_assert(std::is_same<decltype(&ClientMiles::sample_playback_rate), int32_t (*)(ClientMiles::HSAMPLE)>::value, "sample_playback_rate source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_volume_levels), void (*)(ClientMiles::HSAMPLE, float, float)>::value, "set_sample_volume_levels source shape");
static_assert(std::is_same<decltype(&ClientMiles::sample_volume_levels), void (*)(ClientMiles::HSAMPLE, float *, float *)>::value, "sample_volume_levels source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_reverb_levels), void (*)(ClientMiles::HSAMPLE, float, float)>::value, "set_sample_reverb_levels source shape");
static_assert(std::is_same<decltype(&ClientMiles::sample_reverb_levels), void (*)(ClientMiles::HSAMPLE, float *, float *)>::value, "sample_reverb_levels source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_position), void (*)(ClientMiles::HSAMPLE, float, float, float)>::value, "set_sample_3D_position source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_velocity_vector), void (*)(ClientMiles::HSAMPLE, float, float, float)>::value, "set_sample_3D_velocity_vector source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_3D_distances), void (*)(ClientMiles::HSAMPLE, float, float, int32_t)>::value, "set_sample_3D_distances source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_occlusion), void (*)(ClientMiles::HSAMPLE, float)>::value, "set_sample_occlusion source shape");
static_assert(std::is_same<decltype(&ClientMiles::set_sample_obstruction), void (*)(ClientMiles::HSAMPLE, float)>::value, "set_sample_obstruction source shape");
