#ifndef ROBOT_H
#define ROBOT_H

#include <array>
#include <string>
#include <vector>

void update_position(const std::string& action, std::array<int, 3>& position);
void forward(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token);
void backward(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token);
void right(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token);
void left(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token);
std::array<int, 5> sensors(const std::string& run_with_UI, const std::string& token, int border_value);
void move(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token, const std::array<int, 5>& data);
void move_to(const std::vector<char>& path, std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token, const std::vector<std::vector<int>>& maze, int border_value);

#endif // ROBOT_H
