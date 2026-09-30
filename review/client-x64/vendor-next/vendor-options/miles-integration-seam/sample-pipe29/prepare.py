from pathlib import Path
import difflib,shutil
b=Path(__file__).resolve().parent.parent
r=b/'sample-pipe29'; old=b/'pipe-native26/private-source-v1'; stage=b/'sample-pipe28/evidence-v1/stage'
files=['backend-boundary24/pipe/Session.h','backend-boundary24/pipe/ClientMilesPipe.cpp','startup-bridge23/reply.h']
texts={f:(stage/f).read_text() for f in files}
h=texts[files[0]].replace('    void rejectResult();','    bool uncertain() const { return faulted_; }\n    size_t sampleProxyCount() const; // private composition/test observation\n    void rejectResult();')
s=texts[files[1]].replace('#include <vector>','#include <list>')
a=s.index('    enum { Limit = 64 };');z=s.index('\n};',a)
s=s[:a]+'''    typedef std::list<std::unique_ptr<ClientMiles::OwnedSample> > Proxies;
    Proxies proxies;'''+s[z:]
s=s.replace('void Session::rejectResult() {','size_t Session::sampleProxyCount() const { return samples->proxies.size(); }\n\nvoid Session::rejectResult() {')
s=s.replace('    if (session.samples->live())\n        fail(FailureReason::WrongState, "release owned samples before Miles shutdown");\n','')
s=s.replace('    session.request(MilesWire::AIL_shutdown, MilesWire::Call());\n','    session.request(MilesWire::AIL_shutdown, MilesWire::Call());\n    session.samples->proxies.clear(); // confirmed vendor shutdown, local handles expire\n')
s=s.replace('    for (size_t i=0; i<session.samples->proxies.size(); ++i) {\n        OwnedSample *candidate = session.samples->proxies[i].get();','    for (ClientMilesPipe::SampleState::Proxies::iterator i=session.samples->proxies.begin();\n         i!=session.samples->proxies.end(); ++i) {\n        OwnedSample *candidate = i->get();')
s=s.replace('    if (session.samples->proxies.size() == ClientMilesPipe::SampleState::Limit)\n        fail(FailureReason::InputLimit, "sample identity budget exhausted");\n','')
s=s.replace('    StartupBridge::OwnedReply reply = session.request(MilesWire::AIL_allocate_sample_handle, fields);','''    StartupBridge::OwnedReply reply;
    try {
        reply = session.request(MilesWire::AIL_allocate_sample_handle, fields);
    } catch (...) {
        // Only an observed refusal permits discarding the unpublished proxy.
        if (!session.uncertain()) session.samples->proxies.pop_back();
        throw;
    }''')
s=s.replace('    owned.live = false; // only an observed successful reply retires the proxy','''    // Native HSAMPLE lifetime ends here. Caller reuse of that raw pointer is invalid.
    // Wire generations are a separate host/callback obligation, not pointer tokens.
    for (ClientMilesPipe::SampleState::Proxies::iterator i=session.samples->proxies.begin();
         i!=session.samples->proxies.end(); ++i) {
        if (i->get()==&owned) { session.samples->proxies.erase(i); break; }
    }''')
texts[files[0]]=h;texts[files[1]]=s
(r/'patches').mkdir(exist_ok=True)
patch=''.join(''.join(difflib.unified_diff((old/f).read_text().splitlines(True),texts[f].splitlines(True),fromfile='a/'+f,tofile='b/'+f)) for f in files)
(r/'patches/01-owned-sample-client.patch').write_text(patch)
for f in ['prepared_input.h','input-identities.json']:shutil.copyfile(b/'sample-pipe28'/f,r/f)
(r/'check.py').write_text((b/'sample-pipe28/check.py').read_text().replace('sample-pipe28','sample-pipe29'))
t=(b/'sample-pipe28/client_test.cpp').read_text()
t=t.replace('static bool failAllocation=false;','static bool failAllocation=false;\nstatic int allocationsUntilFailure=-1;')
t=t.replace('    if (failAllocation)', '    if (allocationsUntilFailure==0) { allocationsUntilFailure=-1; throw std::bad_alloc(); }\n    if (allocationsUntilFailure>0) --allocationsUntilFailure;\n    if (failAllocation)')
t=t.replace('    unsigned before=script->calls;\n    failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::WrongState);\n    CHECK(script->calls==before);','    CHECK(session.sampleProxyCount()==1);')
t=t.replace('    before=script->calls;\n    failure([&]{ClientMiles::end_sample(sample);},ClientMiles::FailureReason::InvalidArgument);\n    failure([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::InvalidArgument);\n    CHECK(script->calls==before);','    CHECK(session.sampleProxyCount()==0); // released raw pointer is now invalid; never reuse it')
t=t.replace('    CHECK(newer!=sample);','    CHECK(newer!=0 && session.sampleProxyCount()==1);')
a=t.index('static void budget() {');z=t.index('static void retained()',a)
t=t[:a]+'''static void repeated() {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    ClientMiles::HDIGDRIVER driver=start();
    for(unsigned i=0;i<256;++i) {
        auto sample=ClientMiles::allocate_sample_handle(driver);
        CHECK(sample && session.sampleProxyCount()==1);
        ClientMiles::release_sample_handle(sample);
        CHECK(session.sampleProxyCount()==0);
    }
    CHECK(script->allocations==256 && script->releases==256);
    script->refused=StartupBridge::LifecycleRefused;
    failure([&]{ClientMiles::allocate_sample_handle(driver);},ClientMiles::FailureReason::WrongState);
    CHECK(session.sampleProxyCount()==0 && !session.uncertain());
    script->nullAllocation=true;
    CHECK(!ClientMiles::allocate_sample_handle(driver) && session.sampleProxyCount()==0);
    script->nullAllocation=false;
    const unsigned before=script->calls;
    allocationsUntilFailure=1; // proxy allocation succeeds; list publication fails
    bool caught=false;
    try { ClientMiles::allocate_sample_handle(driver); } catch(const std::bad_alloc &) { caught=true; }
    CHECK(caught && allocationsUntilFailure==-1 && script->calls==before && session.sampleProxyCount()==0);
    auto sample=ClientMiles::allocate_sample_handle(driver);
    script->refused=StartupBridge::LifecycleRefused;
    failure([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::WrongState);
    CHECK(session.sampleProxyCount()==1 && !session.uncertain());
    ClientMiles::release_sample_handle(sample);
    CHECK(session.sampleProxyCount()==0);
    ClientMiles::shutdown();session.close();
}
static void shutdownLive(unsigned scenario) {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    auto sample=ClientMiles::allocate_sample_handle(start());
    const unsigned before=script->calls;
    if(scenario==1) {
        script->refused=StartupBridge::LifecycleRefused;
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::WrongState);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1 && !session.uncertain());
        ClientMiles::end_sample(sample); // refusal preserves usable ownership
    }
    if(scenario==2) {
        script->throwsNext=true;
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1 && session.uncertain());
        failure([&]{ClientMiles::end_sample(sample);},ClientMiles::FailureReason::BackendFailed);
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1);
        return; // local abandonment is not vendor cleanup
    }
    ClientMiles::shutdown();
    CHECK(session.sampleProxyCount()==0 && !session.started && session.stopped);
    session.close();
}
'''+t[z:]
t=t.replace('budget(); retained();','repeated(); for(unsigned i=0;i<3;++i) shutdownLive(i); retained();')
(r/'client_test.cpp').write_text(t)
