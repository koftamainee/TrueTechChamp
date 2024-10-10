#ifndef MAZE_H
#define MAZE_H

#include <iostream>
#include <vector>
#include <array>

void show_maze(const std::vector<std::vector<int>>& arr, int type = 2);
void update_maze(const std::array<int, 4>& data, const std::array<int, 3>& position, std::vector<std::vector<int>>& maze);
std::vector<std::vector<int>> processing_maze_data(const std::vector<std::vector<int>>& maze);

#endif // MAZE_H
