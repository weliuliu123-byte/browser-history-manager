#include "Utils.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#include <chrono>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif

using namespace std;

int getIntInput(const string& prompt) {
    // Validate integer input to prevent infinite stream error loops
    int value;
    while (true) {
        cout << prompt;
        if (cin >> value) {
            cin.ignore(10000, '\n'); // Clear trailing newline from input buffer
            return value;
        } else {
            // Recover from non-numeric input
            cout << "  [ERROR] Invalid input. Please enter a number.\n";
            cin.clear();             // Reset fail flags on cin
            cin.ignore(10000, '\n'); // Discard invalid characters in buffer
        }
    }
}

string getStringInput(const string& prompt) {
    string value;
    cout << prompt;
    getline(cin, value);
    return value;
}

string getCurrentTime() {
    // Generate formatted local timestamp
    auto now = chrono::system_clock::now();             // Read current system clock
    auto in_time_t = chrono::system_clock::to_time_t(now);
    stringstream ss;
    ss << put_time(localtime(&in_time_t), "%Y-%m-%d %H:%M:%S"); // Format: YYYY-MM-DD HH:MM:SS
    return ss.str();
}

double getActualRAMUsageKB() {
    // Query actual process working-set memory via Windows PSAPI
#ifdef _WIN32
    static HMODULE hPsapi = LoadLibraryA("psapi.dll"); // Cache psapi.dll handle once across calls
    if (hPsapi) {
        typedef BOOL(WINAPI* GETPROCESSMEMORYINFO)(HANDLE, PPROCESS_MEMORY_COUNTERS, DWORD);
        static GETPROCESSMEMORYINFO getMemInfo = (GETPROCESSMEMORYINFO)GetProcAddress(hPsapi, "GetProcessMemoryInfo");
        if (getMemInfo) {
            PROCESS_MEMORY_COUNTERS pmc;
            if (getMemInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
                // Return resident WorkingSetSize in KiB
                return pmc.WorkingSetSize / 1024.0; // Convert bytes to KiB
            }
        }
    }
#endif
    return 0.0;
}

