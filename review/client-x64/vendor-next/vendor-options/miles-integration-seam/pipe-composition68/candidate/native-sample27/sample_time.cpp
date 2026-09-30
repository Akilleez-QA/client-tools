#include "sample_time.h"

namespace SampleTime27
{
Observations inspectDuration(ClientMiles::HDIGDRIVER driver, const char *extension,
                             const void *fileImage, int32_t signedFileBytes)
{
    Observations result;
    // Validate the original signed extent before its U32 SDK conversion. The
    // original helper's s_installed policy remains in its caller, not this seam.
    if (!extension || !fileImage || signedFileBytes <= 0)
        return result;

    ClientMiles::HSAMPLE sample = ClientMiles::allocate_sample_handle(driver);
    if (!sample)
        return result;
    result.allocated = true;
    result.bindingResult = ClientMiles::set_named_sample_file(
        sample, extension, fileImage, static_cast<uint32_t>(signedFileBytes), 0);
    if (result.bindingResult)
    {
        ClientMiles::sample_ms_position(sample, &result.totalMilliseconds,
                                        &result.currentMilliseconds);
        ClientMiles::end_sample(sample);
    }
    // Every nonnull allocation is released on both normal binding outcomes.
    // The caller's suffix/image stay alive until this call has returned.
    ClientMiles::release_sample_handle(sample);
    return result;
}
}
