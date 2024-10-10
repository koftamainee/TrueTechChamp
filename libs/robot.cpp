#include "robot.h"
#include <iostream>
#include <curl/curl.h> // Ensure you have libcurl installed for HTTP requests
#include <json/json.h> // You need a JSON library like jsoncpp

void update_position(const std::string& action, std::array<int, 3>& position) {
    int yaw = position[2] % 360;

    if (yaw == 0 || abs(yaw) == 180) {
        position[1] += (yaw == 0 ? 1 : -1);
    } else if (abs(yaw) == 90) {
        position[0] += (yaw == 90 ? 1 : -1);
    }

    if (action == "right") {
        position[2] += 90;
    } else if (action == "left") {
        position[2] -= 90;
    }

    std::cout << "Movement: " << action << ", position: [" << position[0] << ", " << position[1] << "], normalized yaw: " << yaw << "\n";
}

void forward(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token) {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/forward?token=" + token;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

void backward(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token) {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/backward?token=" + token;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

void right(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token) {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/right?token=" + token;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

void left(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token) {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/left?token=" + token;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

std::array<int, 5> sensors(const std::string& run_with_UI, const std::string& token, int border_value) {
    CURL* curl = curl_easy_init();
    std::array<int, 5> sensor_data;

    if (curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/sensor-data?token=" + token;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        curl_easy_perform(curl);

        // You would typically parse the response here, using a JSON library.
        // Example response processing:
        // sensor_data = parse_sensor_data(response);

        curl_easy_cleanup(curl);
    }

    return sensor_data; // Replace with actual data
}

void move(std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token, const std::array<int, 5>& data) {
    // Logic for movement based on sensor data
}

void move_to(const std::vector<char>& path, std::array<int, 3>& position, const std::string& run_with_UI, const std::string& token, const std::vector<std::vector<int>>& maze, int border_value) {
    for (char step : path) {
        if (step == 'F') {
            forward(position, run_with_UI, token);
        } else if (step == 'B') {
            backward(position, run_with_UI, token);
        } else if (step == 'R') {
            right(position, run_with_UI, token);
        } else if (step == 'L') {
            left(position, run_with_UI, token);
        }
        // Update the position after each move
        update_position(std::string(1, step), position);
    }
}
