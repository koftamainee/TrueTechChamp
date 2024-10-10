#include "maze.h"
#include <iomanip>

void show_maze(const std::vector<std::vector<int>>& arr, int type) {
    int l = arr.size();
    std::cout << "  ";
    for (int i = 0; i < l; i++) {
        std::cout << std::setw(3) << i;
    }
    std::cout << "\n\n";
    
    auto ch = [](int x) { return x ? "* " : "  "; };
    for (int i = 0; i < l; i++) {
        std::cout << std::setw(2) << (l - i - 1);
        if (type == 1) {
            std::cout << arr[i];
        } else {
            for (auto val : arr[i]) {
                std::cout << ch(val);
            }
        }
        std::cout << std::setw(2) << (l - i - 1) << "\n";
    }

    std::cout << "  ";
    for (int i = 0; i < l; i++) {
        std::cout << std::setw(3) << i;
    }
    std::cout << "\n";
}

void update_maze(const std::array<int, 4>& data, const std::array<int, 3>& position, std::vector<std::vector<int>>& maze) {
    std::cout << "Walls:\n";
    int yaw = (position[2] % 360 + 360) % 360 / 90; // Normalize yaw
    int x = position[0] * 2 + 1;
    int y = (15 - position[1]) * 2 + 1;

    std::array<int, 4> wf = {1, 4, 3, 2};
    std::array<int, 4> wr = {2, 1, 4, 3};
    std::array<int, 4> wb = {3, 2, 1, 4};
    std::array<int, 4> wl = {4, 3, 2, 1};

    if (!data[wf[yaw]]) {
        maze[y - 1][x] = 1;
        maze[y - 1][x - 1] = 1;
        maze[y - 1][x + 1] = 1;
        std::cout << "wall forward\n";
    }
    if (!data[wb[yaw]]) {
        maze[y + 1][x] = 1;
        maze[y + 1][x + 1] = 1;
        maze[y + 1][x - 1] = 1;
        std::cout << "wall backward\n";
    }
    if (!data[wl[yaw]]) {
        maze[y][x - 1] = 1;
        maze[y + 1][x - 1] = 1;
        maze[y - 1][x - 1] = 1;
        std::cout << "wall left\n";
    }
    if (!data[wr[yaw]]) {
        maze[y][x + 1] = 1;
        maze[y + 1][x + 1] = 1;
        maze[y - 1][x + 1] = 1;
        std::cout << "wall right\n";
    }
    std::cout << "\n";
}

std::vector<std::vector<int>> processing_maze_data(const std::vector<std::vector<int>>& maze) {
    std::vector<std::vector<int>> result_maze(16, std::vector<int>(16, 0));
    
    for (int i = 1; i < 32; i += 2) {
        for (int j = 1; j < 32; j += 2) {
            std::array<int, 4> dt = {
                maze[i - 1][j], maze[i][j + 1], maze[i + 1][j], maze[i][j - 1]
            };
            int ri = i / 2;
            int rj = j / 2;
            int res = -1;

            int sum_dt = dt[0] + dt[1] + dt[2] + dt[3];
            if (sum_dt == 0) {
                res = 0;
            } else if (sum_dt == 1) {
                if (dt[3] == 1) res = 1;
                else if (dt[0] == 1) res = 2;
                else if (dt[1] == 1) res = 3;
                else if (dt[2] == 1) res = 4;
            } else if (sum_dt == 2) {
                if (dt[2] == 1 && dt[3] == 1) res = 5;
                else if (dt[2] == 1 && dt[1] == 1) res = 6;
                else if (dt[0] == 1 && dt[1] == 1) res = 7;
                else if (dt[0] == 1 && dt[3] == 1) res = 8;
                else if (dt[3] == 1 && dt[1] == 1) res = 9;
                else if (dt[0] == 1 && dt[2] == 1) res = 10;
            } else if (sum_dt == 3) {
                if (dt[3] == 0) res = 11;
                else if (dt[2] == 0) res = 12;
                else if (dt[1] == 0) res = 13;
                else if (dt[0] == 0) res = 14;
            } else if (sum_dt == 4) {
                res = 15;
            }
            result_maze[ri][rj] = res;
        }
    }

    return result_maze;
}
