#define NOMINMAX
#include <bits/stdc++.h>
#include <windows.h>
#include <filesystem>
#define endl '\n'
using namespace std;
using ll = long long;
namespace fs = std::filesystem;

struct Res
{
    DWORD code;
    bool tle;
};

wstring quote(const wstring &s)
{
    wstring t = L"\"";
    int n = 0;
    for (wchar_t c : s)
    {
        if (c == L'\\')
            ++n;
        else
        {
            t.append(c == L'\"' ? n * 2 + 1 : n, L'\\');
            t += c;
            n = 0;
        }
    }
    t.append(n * 2, L'\\');
    return t + L"\"";
}

HANDLE openfile(const fs::path &p, bool wr)
{
    SECURITY_ATTRIBUTES sa = {sizeof(sa), nullptr, TRUE};
    HANDLE h = CreateFileW(p.c_str(), wr ? GENERIC_WRITE : GENERIC_READ,
                           FILE_SHARE_READ, &sa, wr ? CREATE_ALWAYS : OPEN_EXISTING,
                           FILE_ATTRIBUTE_NORMAL, nullptr);
    if (h == INVALID_HANDLE_VALUE)
        throw runtime_error("Cannot open file: " + p.u8string());
    return h;
}

Res run(const fs::path &exe, const wstring &arg, const fs::path &in,
        const fs::path &out, const fs::path &err, DWORD ms)
{
    HANDLE a = openfile(in, false), b = openfile(out, true), c = openfile(err, true);
    STARTUPINFOW si = {};
    PROCESS_INFORMATION pi = {};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = a;
    si.hStdOutput = b;
    si.hStdError = c;
    wstring cmd = quote(exe.wstring());
    if (!arg.empty())
        cmd += L" " + quote(arg);
    BOOL ok = CreateProcessW(exe.c_str(), cmd.data(), nullptr, nullptr, TRUE,
                             CREATE_NO_WINDOW, nullptr, nullptr, &si, &pi);
    DWORD e = GetLastError();
    CloseHandle(a);
    CloseHandle(b);
    CloseHandle(c);
    if (!ok)
        throw runtime_error("Cannot start process, Windows error " + to_string(e));
    DWORD s = WaitForSingleObject(pi.hProcess, ms);
    bool tle = s == WAIT_TIMEOUT;
    if (tle)
    {
        if (!TerminateProcess(pi.hProcess, 124))
            throw runtime_error("Cannot terminate timed-out process");
        if (WaitForSingleObject(pi.hProcess, 5000) != WAIT_OBJECT_0)
            throw runtime_error("Timed-out process did not stop");
    }
    else if (s != WAIT_OBJECT_0)
    {
        TerminateProcess(pi.hProcess, 125);
        throw runtime_error("Cannot wait for process");
    }
    DWORD code = 0;
    if (!GetExitCodeProcess(pi.hProcess, &code))
        throw runtime_error("Cannot read process exit code");
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return {code, tle};
}

bool same(const fs::path &a, const fs::path &b)
{
    ifstream f(a), g(b);
    if (!f || !g)
        throw runtime_error("Cannot read output files");
    string x, y;
    while (true)
    {
        bool p = bool(f >> x), q = bool(g >> y);
        if (f.bad() || g.bad())
            throw runtime_error("Output read error");
        if (p != q)
            return false;
        if (!p)
            return true;
        if (x != y)
            return false;
    }
}

bool check(Res r, const string &s, ofstream &log)
{
    log << s << " exit=" << r.code << " timeout=" << r.tle << endl;
    log.flush();
    if (r.tle || r.code)
    {
        cout << "STOP: " << s << (r.tle ? " timed out" : " exited with error") << endl;
        return false;
    }
    return true;
}

int wmain(int argc, wchar_t **argv)
{
    if (argc != 7)
    {
        cout << "Usage: stress.exe SOL.exe BRUTE.exe GEN.exe ROUNDS SEED TIMEOUT_MS" << endl;
        cout << "GEN receives one seed argument. Outputs are compared by whitespace-separated tokens." << endl;
        return argc == 1 ? 0 : 2;
    }
    try
    {
        fs::path sol = fs::absolute(argv[1]), brute = fs::absolute(argv[2]);
        fs::path gen = fs::absolute(argv[3]);
        ll n = stoll(argv[4]);
        unsigned long long seed = stoull(argv[5]), ms = stoull(argv[6]);
        if (n < 1 || n > 1000000 || ms < 1 || ms > 3600000 ||
            (unsigned long long)(n - 1) > ULLONG_MAX - seed)
            throw runtime_error("Invalid rounds, seed range or timeout");
        if (!fs::is_regular_file(sol) || !fs::is_regular_file(brute) || !fs::is_regular_file(gen))
            throw runtime_error("One or more executables do not exist");
        fs::path dir = fs::current_path() / "work" / "stress" /
                       (to_string(GetCurrentProcessId()) + "-" + to_string(chrono::steady_clock::now().time_since_epoch().count()));
        if (!fs::create_directories(dir))
            throw runtime_error("Run directory already exists");
        cout << "Files: " << dir.u8string() << endl;
        ofstream empty(dir / "empty.in");
        if (!empty)
            throw runtime_error("Cannot create empty input");
        empty.close();
        for (ll i = 0; i < n; ++i)
        {
            unsigned long long cur = seed + i;
            ofstream log(dir / "case.txt");
            if (!log)
                throw runtime_error("Cannot write case metadata");
            log << "round=" << i + 1 << " seed=" << cur << " timeout_ms=" << ms << endl;
            log << "sol=" << sol.u8string() << "\nbrute=" << brute.u8string()
                << "\ngen=" << gen.u8string() << endl;
            if (!check(run(gen, to_wstring(cur), dir / "empty.in", dir / "case.in",
                           dir / "gen.err", DWORD(ms)),
                       "gen", log))
                return 1;
            if (!check(run(sol, L"", dir / "case.in", dir / "sol.out",
                           dir / "sol.err", DWORD(ms)),
                       "sol", log))
                return 1;
            if (!check(run(brute, L"", dir / "case.in", dir / "brute.out",
                           dir / "brute.err", DWORD(ms)),
                       "brute", log))
                return 1;
            if (!same(dir / "sol.out", dir / "brute.out"))
            {
                log << "result=WA" << endl;
                cout << "STOP: mismatch at round " << i + 1 << ", seed " << cur << endl;
                return 1;
            }
            log << "result=matched" << endl;
        }
        cout << "All " << n << " cases matched. Last case retained." << endl;
        return 0;
    }
    catch (const exception &e)
    {
        cerr << "STOP: " << e.what() << endl;
        return 2;
    }
}
