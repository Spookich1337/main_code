#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

const int INF = INT_MAX / 2;

std::vector<int> exactTSP(const std::vector<std::vector<int>>& dist, int n, bool debug);

std::vector<int> approxTSP(const std::vector<std::vector<int>>& dist, int n, bool debug);