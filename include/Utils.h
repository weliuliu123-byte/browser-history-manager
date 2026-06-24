#ifndef UTILS_H
#define UTILS_H

#include <string>

std::string getCurrentTime();
int getIntInput(const std::string& prompt);
std::string getStringInput(const std::string& prompt);
double getActualRAMUsageKB();

#endif

