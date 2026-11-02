// Build for Windows x64. This bridge runs only on MuMuPlayer's GUI thread.
// No VM/game process, executable file, or Qt DLL on disk is modified.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>

static const wchar_t* StatusName = L"Codex.MuMuOpacity.QtBridge.Status.20261030";
static const wchar_t* AlphaName = L"Codex.MuMuOpacity.QtBridge.RetainedAlpha.20261030";
static const wchar_t* ResetCountName = L"Codex.MuMuOpacity.QtBridge.PreventedResetCount.20261030";
static const WPARAM Cookie = 0x4D550000;
static thread_local bool applying = false;

static bool matchesOpacity(HWND window, BYTE alpha) {
    DWORD color = 0, flags = 0;
    BYTE actual = 0;
    const bool layered = (GetWindowLongPtrW(window, GWL_EXSTYLE) & WS_EX_LAYERED) != 0;
    return (alpha == 255 && !layered) ||
        (GetLayeredWindowAttributes(window, &color, &actual, &flags) && (flags & LWA_ALPHA) && actual == alpha);
}

static ULONG_PTR applyQt(HWND window, BYTE alpha) {
    if (applying) return 4;
    HMODULE widgets = GetModuleHandleW(L"Qt5Widgets.dll");
    typedef void* (*FindWidget)(uint64_t);
    typedef void (*SetOpacity)(void*, double);
    FindWidget find = widgets ? reinterpret_cast<FindWidget>(GetProcAddress(widgets, "?find@QWidget@@SAPEAV1@_K@Z")) : nullptr;
    SetOpacity set = widgets ? reinterpret_cast<SetOpacity>(GetProcAddress(widgets, "?setWindowOpacity@QWidget@@QEAAXN@Z")) : nullptr;
    if (!find || !set) return 2;
    void* widget = find(reinterpret_cast<uint64_t>(window));
    if (!widget) return 3;
    applying = true;
    const double opacity = double(alpha) / 255.0;
    set(widget, opacity);
    if (!matchesOpacity(window, alpha)) {
        // Bypass stale Qt caches without changing the rounded alpha byte.
        const double nudge = alpha < 255 ? (double(alpha) + 0.1) / 255.0 : 254.9 / 255.0;
        set(widget, nudge);
        set(widget, opacity);
    }
    applying = false;
    return 1;
}

static BYTE retainedAlpha(HWND window) {
    const ULONG_PTR value = reinterpret_cast<ULONG_PTR>(GetPropW(window, AlphaName));
    return value >= 1 && value <= 255 ? BYTE(value - 1) : BYTE(255);
}

static void ensureBeforePaint(HWND window) {
    if (applying) return;
    const BYTE alpha = retainedAlpha(window);
    if (alpha < 255 && !matchesOpacity(window, alpha)) applyQt(window, alpha);
}

extern "C" __declspec(dllexport) LRESULT CALLBACK MuMuOpacityHook(int code, WPARAM wp, LPARAM lp) {
    if (code >= 0) {
        const CWPSTRUCT* msg = reinterpret_cast<const CWPSTRUCT*>(lp);
        const UINT command = RegisterWindowMessageW(L"Codex.MuMuOpacity.QtBridge.Apply.20261030");
        if (msg && msg->message == command && (msg->wParam & ~WPARAM(255)) == Cookie) {
            wchar_t file[MAX_PATH] = {};
            GetModuleFileNameW(nullptr, file, MAX_PATH);
            const wchar_t* base = file;
            for (const wchar_t* p = file; *p; ++p) if (*p == L'\\' || *p == L'/') base = p + 1;
            if (lstrcmpiW(base, L"MuMuPlayer.exe") == 0) {
                const BYTE alpha = BYTE(msg->wParam & 255);
                if (alpha < 255) SetPropW(msg->hwnd, AlphaName, reinterpret_cast<HANDLE>(ULONG_PTR(alpha) + 1));
                else RemovePropW(msg->hwnd, AlphaName);
                const ULONG_PTR result = applyQt(msg->hwnd, alpha);
                if (result != 1) RemovePropW(msg->hwnd, AlphaName);
                SetPropW(msg->hwnd, StatusName, reinterpret_cast<HANDLE>(result));
            }
        } else if (msg && !applying) {
            if (msg->message == WM_STYLECHANGING && int(msg->wParam) == GWL_EXSTYLE && retainedAlpha(msg->hwnd) < 255) {
                STYLESTRUCT* styles = reinterpret_cast<STYLESTRUCT*>(msg->lParam);
                if (styles && !(styles->styleNew & WS_EX_LAYERED)) {
                    // Preserve the requested layer before a reset reaches DWM.
                    // This avoids showing an opaque frame then repairing it later.
                    styles->styleNew |= WS_EX_LAYERED;
                    const ULONG_PTR count = reinterpret_cast<ULONG_PTR>(GetPropW(msg->hwnd, ResetCountName));
                    SetPropW(msg->hwnd, ResetCountName, reinterpret_cast<HANDLE>(count + 1));
                }
            }
            if ((msg->message == WM_SHOWWINDOW && msg->wParam) || msg->message == WM_PAINT || msg->message == WM_NCPAINT || msg->message == WM_ERASEBKGND)
                ensureBeforePaint(msg->hwnd);
            if (msg->message == WM_WINDOWPOSCHANGING) {
                const WINDOWPOS* position = reinterpret_cast<const WINDOWPOS*>(msg->lParam);
                if (position && (position->flags & SWP_SHOWWINDOW)) ensureBeforePaint(msg->hwnd);
            }
        }
    }
    return CallNextHookEx(nullptr, code, wp, lp);
}

extern "C" __declspec(dllexport) LRESULT CALLBACK MuMuOpacityAfterHook(int code, WPARAM wp, LPARAM lp) {
    if (code >= 0 && !applying) {
        const CWPRETSTRUCT* msg = reinterpret_cast<const CWPRETSTRUCT*>(lp);
        if (msg && (msg->message == WM_SHOWWINDOW || msg->message == WM_STYLECHANGED || msg->message == WM_WINDOWPOSCHANGED))
            ensureBeforePaint(msg->hwnd);
    }
    return CallNextHookEx(nullptr, code, wp, lp);
}

BOOL WINAPI DllMain(HINSTANCE, DWORD, LPVOID) { return TRUE; }
