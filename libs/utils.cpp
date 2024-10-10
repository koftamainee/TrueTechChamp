#include <iostream>
#include <vector>
#include <cmath>
#include <curl/curl.h> // For HTTP requests
#include <nlohmann/json.hpp> // For JSON handling

using json = nlohmann::json;

// Normalize the angle to the range of -180 to 180
int normalize_angle(int angle) {
    int normalized_angle = (angle + 180) % 360 - 180;
    return normalized_angle;
}

// Function to send a matrix to a specified API endpoint
json send_matrix(const json& matrix) {
    CURL* curl;
    CURLcode res;
    json response_json;

    // Initialize cURL
    curl = curl_easy_init();
    if(curl) {
        std::string url = "http://127.0.0.1:8801/api/v1/matrix/send?token=(token)";
        
        // Set options for cURL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, matrix.dump().c_str());
        
        // Set content type to JSON
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        
        // Send the request and get the response
        res = curl_easy_perform(curl);
        
        // Handle the response (you might need to implement a proper response handler)
        if(res == CURLE_OK) {
            // If you need to read the response into response_json, you can implement a write callback
            // For simplicity, this part is omitted.
        }

        // Clean up
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    return response_json; // Return the JSON response
}

// Calculate the new point based on the current position and move direction
std::vector<int> calculate_point(const std::vector<int>& position, const std::string& move) {
    int yaw = normalize_angle(position[2]);
    std::vector<int> coords = {position[0], position[1]};

    if (yaw == 0) {
        if (move == "f") return {coords[0], coords[1] + 1};
        else if (move == "r") return {coords[0] + 1, coords[1]};
        else if (move == "l") return {coords[0] - 1, coords[1]};
        else if (move == "b") return {coords[0], coords[1] - 1};
    } else if (yaw == 90) {
        if (move == "f") return {coords[0] + 1, coords[1]};
        else if (move == "r") return {coords[0], coords[1] - 1};
        else if (move == "l") return {coords[0], coords[1] + 1};
        else if (move == "b") return {coords[0] - 1, coords[1]};
    } else if (yaw == -90) {
        if (move == "f") return {coords[0] - 1, coords[1]};
        else if (move == "r") return {coords[0], coords[1] + 1};
        else if (move == "l") return {coords[0], coords[1] - 1};
        else if (move == "b") return {coords[0] + 1, coords[1]};
    } else if (abs(yaw) == 180) {
        if (move == "f") return {coords[0], coords[1] - 1};
        else if (move == "r") return {coords[0] - 1, coords[1]};
        else if (move == "l") return {coords[0] + 1, coords[1]};
        else if (move == "b") return {coords[0], coords[1] + 1};
    }

    return coords; // Return the original coordinates if no move matches
}
