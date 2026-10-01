#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <string.h>

// Extracted caller/registry contract. No production loader, RegistryKey method,
// provider DLL, hardware call, or preexisting registry key is used by this probe.
struct Guarded
{
    unsigned char before[8];
    char path[512];
    unsigned char after[8];
};

static unsigned failures = 0;
static unsigned queries = 0;

static void require(bool condition, char const *what, unsigned caseId)
{
    if (!condition)
    {
        ++failures;
        printf("FAIL case=%u %s\n", caseId, what);
    }
}

static void queryCase(HKEY key, unsigned caseId, char const *dll,
    unsigned length, bool terminated, bool candidate)
{
    unsigned const bound = 512u - static_cast<unsigned>(strlen(dll)) - 2u;
    DWORD const capacity = bound + (candidate ? 1u : 0u);
    DWORD const registryBytes = length + (terminated ? 1u : 0u);
    bool const expectedQuerySuccess = registryBytes <= capacity;
    bool const expectedAppend = expectedQuerySuccess && length <= bound;
    Guarded g;
    memset(&g, 0xa5, sizeof(g));
    // This is the existing helper's initial clear, using the passed byte capacity.
    memset(g.path, 0, capacity);
    DWORD bytes = capacity;
    DWORD type = 0;
    LONG const result = RegQueryValueExA(key, "Path", 0, &type,
        reinterpret_cast<LPBYTE>(g.path), &bytes);
    ++queries;
    require(result == (expectedQuerySuccess ? ERROR_SUCCESS : ERROR_MORE_DATA), "query outcome", caseId);
    require(bytes == registryBytes, "registry byte count", caseId);
    require(type == REG_SZ, "registry type", caseId);
    bool appended = false;
    if (result == ERROR_SUCCESS)
    {
        require(bytes <= capacity && bytes < sizeof(g.path), "returned extent", caseId);
        if (bytes <= capacity && bytes < sizeof(g.path))
        {
            // Match the existing helper's explicit extra terminator on success.
            g.path[bytes] = 0;
            require(strlen(g.path) == length, "read character count", caseId);
            char beforeAppend[512];
            memcpy(beforeAppend, g.path, sizeof(g.path));
            if (strlen(g.path) <= bound)
            {
                strcat(g.path, "\\");
                strcat(g.path, dll);
                appended = true;
            }
            require(appended == expectedAppend, "append decision", caseId);
            if (appended)
            {
                unsigned const total = length + 1u + static_cast<unsigned>(strlen(dll));
                require(total < sizeof(g.path), "final extent", caseId);
                require(strlen(g.path) == total && g.path[total] == 0, "final terminator", caseId);
                require(g.path[length] == '\\' && strcmp(g.path + length + 1, dll) == 0, "exact DLL suffix", caseId);
                for (unsigned i = 0; i != length; ++i)
                    require(g.path[i] == 'x', "prefix preserved", caseId);
            }
            else
                require(memcmp(beforeAppend, g.path, sizeof(g.path)) == 0, "rejection leaves append buffer unchanged", caseId);
        }
    }
    else
        require(!expectedAppend, "unexpected failed fitting query", caseId);
    for (unsigned i = 0; i != 8; ++i)
        require(g.before[i] == 0xa5 && g.after[i] == 0xa5, "outer sentinels", caseId);
    printf("QUERY case=%u mode=%s capacity=%lu result=%ld bytes=%lu append=%u\n",
        caseId, candidate ? "candidate" : "old", capacity, result, bytes, appended ? 1u : 0u);
}

int main(int argc, char **argv)
{
#if defined(_WIN64)
    char const *arch = "x64";
#else
    char const *arch = "Win32";
#endif
    if (argc != 2 || strlen(argv[1]) > 80)
        return 90;
    char keyPath[180];
    int const written = sprintf_s(keyPath, sizeof(keyPath),
        "Software\\SWGSourceTrackIRPRCheck-%s-%s", argv[1], arch);
    if (written <= 0)
        return 91;
    HKEY key = 0;
    DWORD disposition = 0;
    LONG const created = RegCreateKeyExA(HKEY_CURRENT_USER, keyPath, 0, 0,
        REG_OPTION_NON_VOLATILE, KEY_QUERY_VALUE | KEY_SET_VALUE, 0, &key, &disposition);
    printf("KEY path=%s create=%ld disposition=%lu\n", keyPath, created, disposition);
    if (created != ERROR_SUCCESS)
        return 92;
    if (disposition != REG_CREATED_NEW_KEY)
    {
        RegCloseKey(key);
        printf("FAIL preexisting key left unchanged\n");
        return 93;
    }
    unsigned cases = 0;
    char const *names[] = { "NPClient.dll", "NPClient64.dll" };
    for (unsigned name = 0; name != 2; ++name)
    {
        unsigned const bound = 512u - static_cast<unsigned>(strlen(names[name])) - 2u;
        unsigned const lengths[] = { 1, bound - 1, bound, bound + 1 };
        for (unsigned term = 0; term != 2; ++term)
        {
            bool const terminated = term == 0;
            for (unsigned sample = 0; sample != 4; ++sample)
            {
                unsigned const length = lengths[sample];
                char value[512];
                memset(value, 'x', sizeof(value));
                if (terminated)
                    value[length] = 0;
                DWORD const bytes = length + (terminated ? 1u : 0u);
                LONG const set = RegSetValueExA(key, "Path", 0, REG_SZ,
                    reinterpret_cast<BYTE const *>(value), bytes);
                require(set == ERROR_SUCCESS, "set isolated REG_SZ", cases);
                printf("CASE id=%u dll=%s chars=%u terminated=%u registryBytes=%lu set=%ld\n",
                    cases, names[name], length, terminated ? 1u : 0u, bytes, set);
                if (set == ERROR_SUCCESS)
                {
                    queryCase(key, cases, names[name], length, terminated, false);
                    queryCase(key, cases, names[name], length, terminated, true);
                }
                ++cases;
            }
        }
    }
    LONG const closed = RegCloseKey(key);
    LONG const removed = RegDeleteKeyA(HKEY_CURRENT_USER, keyPath);
    HKEY after = 0;
    LONG const absent = RegOpenKeyExA(HKEY_CURRENT_USER, keyPath, 0, KEY_QUERY_VALUE, &after);
    if (absent == ERROR_SUCCESS)
        RegCloseKey(after);
    require(closed == ERROR_SUCCESS && removed == ERROR_SUCCESS && absent == ERROR_FILE_NOT_FOUND,
        "owned key cleanup and absence", cases);
    require(cases == 16 && queries == 32, "exact corpus count", cases);
    printf("CLEANUP close=%ld delete=%ld absent=%ld\n", closed, removed, absent);
    printf("RESULT arch=%s cases=%u queries=%u failures=%u keyDeleted=%u\n",
        arch, cases, queries, failures, removed == ERROR_SUCCESS && absent == ERROR_FILE_NOT_FOUND ? 1u : 0u);
    return failures ? 1 : 0;
}
