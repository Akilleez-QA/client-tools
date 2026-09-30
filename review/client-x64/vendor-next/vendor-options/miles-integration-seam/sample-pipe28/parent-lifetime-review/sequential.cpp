#define main frozen_suite_main
#include "../evidence-v1/stage/sample-pipe28/client_test.cpp"
#undef main
int main() {
    Script *script = new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    unsigned completed = 0;
    try {
        ClientMiles::HDIGDRIVER driver = start();
        for (; completed < 65; ++completed) {
            ClientMiles::HSAMPLE sample = ClientMiles::allocate_sample_handle(driver);
            CHECK(sample != 0);
            ClientMiles::release_sample_handle(sample);
        }
        ClientMiles::shutdown(); session.close();
        std::printf("PASS 65 sequential allocated/released samples\n");
        return 0;
    } catch (const ClientMiles::Failure &e) {
        std::fprintf(stderr, "FAIL completed=%u allocations=%u releases=%u reason=%d: %s\n",
                     completed, script->allocations, script->releases, static_cast<int>(e.reason()), e.what());
        return 1;
    }
}
