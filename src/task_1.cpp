#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <curl/curl.h>
#include <json/json.h> // Make sure to include the JSON library

// Function prototypes
void load_env();
std::string get_token();
std::vector<int> sensors(bool run_with_UI, const std::string& token, int border_value);
void update_graph(std::unordered_map<std::string, std::vector<int>>& maze_graph, const std::vector<int>& data, const std::vector<int>& position);
void update_maze(const std::vector<int>& data, const std::vector<int>& position, std::vector<std::vector<int>>& maze);
std::vector<int> calculate_point(const std::vector<int>& position, const std::string& direction);
void forward(std::vector<int>& position, bool run_with_UI, const std::string& token);
void backward(std::vector<int>& position, bool run_with_UI, const std::string& token);
void right(std::vector<int>& position, bool run_with_UI, const std::string& token);
void left(std::vector<int>& position, bool run_with_UI, const std::string& token);
std::string send_matrix(const std::vector<std::vector<int>>& matrix);
void show_maze(const std::vector<std::vector<int>>& maze);
std::vector<std::vector<int>> processing_maze_data(const std::vector<std::vector<int>>& maze);

int main() {
    load_env();
    std::string token = get_token();

    std::vector<int> position = {0, 0, 0};
    std::unordered_map<std::string, std::vector<int>> maze_graph;
    std::vector<std::string> path_stack;
    std::vector<std::string> passed_forks;
    bool run_with_UI = true;
    run_with_UI = false; // Just an example; adjust as necessary
    std::vector<std::vector<int>> maze(33, std::vector<int>(33, 1));
    for (int i = 1; i <= 31; ++i) {
        maze[i].assign(31, 0);
        maze[i][0] = maze[i][32] = 1;
    }
    int cells_cnt = 0;
    int border_value = 65;

    while (cells_cnt != 256) {
        std::cout << "Forks stack: ";
        for (const auto& fork : path_stack) {
            std::cout << fork << " ";
        }
        std::cout << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(40));
        std::vector<int> data = sensors(run_with_UI, token, border_value);
        std::vector<int> coords = {position[0], position[1]};
        
        // Check if coords already passed
        if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(coords[0]) + "," + std::to_string(coords[1])) == passed_forks.end()) {
            passed_forks.push_back(std::to_string(coords[0]) + "," + std::to_string(coords[1]));
            cells_cnt++;
        }

        update_graph(maze_graph, data, position);

        std::cout << "------------------------" << std::endl;
        std::cout << "Cells_cnt: " << cells_cnt << std::endl;
        update_maze(data, position, maze);

        if ((data[1] + data[2] + data[4]) > 1 && data[3] == 1) {
            if (data[1] == 1 && data[2] == 1 && data[4] == 1) {
                auto calculated_coords = calculate_point(position, "r");
                if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1])) == passed_forks.end()) {
                    path_stack.push_back("[" + std::to_string(calculated_coords[0]) + ", " + std::to_string(calculated_coords[1]) + "]");
                    passed_forks.push_back(std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1]));
                }

                calculated_coords = calculate_point(position, "l");
                if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1])) == passed_forks.end()) {
                    path_stack.push_back("[" + std::to_string(calculated_coords[0]) + ", " + std::to_string(calculated_coords[1]) + "]");
                    passed_forks.push_back(std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1]));
                }

                forward(position, run_with_UI, token);

            } else if (data[1] == 1 && data[2] == 1 && data[4] == 0) {
                auto calculated_coords = calculate_point(position, "r");
                if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1])) == passed_forks.end()) {
                    path_stack.push_back("[" + std::to_string(calculated_coords[0]) + ", " + std::to_string(calculated_coords[1]) + "]");
                    passed_forks.push_back(std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1]));
                }

                forward(position, run_with_UI, token);

            } else if (data[1] == 1 && data[2] == 0 && data[4] == 1) {
                auto calculated_coords = calculate_point(position, "l");
                if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1])) == passed_forks.end()) {
                    path_stack.push_back("[" + std::to_string(calculated_coords[0]) + ", " + std::to_string(calculated_coords[1]) + "]");
                    passed_forks.push_back(std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1]));
                }

                forward(position, run_with_UI, token);

            } else if (data[1] == 0 && data[2] == 1 && data[4] == 1) {
                auto calculated_coords = calculate_point(position, "l");
                if (std::find(passed_forks.begin(), passed_forks.end(), std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1])) == passed_forks.end()) {
                    path_stack.push_back("[" + std::to_string(calculated_coords[0]) + ", " + std::to_string(calculated_coords[1]) + "]");
                    passed_forks.push_back(std::to_string(calculated_coords[0]) + "," + std::to_string(calculated_coords[1]));
                }

                right(position, run_with_UI, token);
                forward(position, run_with_UI, token);
            }

        } else {
            if ((data[1] + data[2] + data[4]) == 0) {
                std::cout << "Moving to " << path_stack.back() << "..." << std::endl;
                // Call A* algorithm and move to the new position
                // Implement the a_star function to retrieve move_path
                std::vector<int> move_path; // replace this with actual path calculation
                move_to(move_path, position, run_with_UI, token, maze, border_value);
            } else {
                move(position, run_with_UI, token, data);
            }
        }
    }

    show_maze(maze);
    auto matrix = processing_maze_data(maze);
    std::cout << "Answer matrix: ";
    for (const auto& row : matrix) {
        for (const auto& val : row) {
            std::cout << val << " ";
        }
    }
    std::cout << std::endl;

    std::string res = send_matrix(matrix);
    std::cout << "Score: " << res << " / 256" << std::endl;

    return 0;
}

// Implement the other necessary functions below...
