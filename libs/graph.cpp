#include "graph.h"

// Constructor
Graph::Graph() {}

// Add a vertex to the graph
void Graph::add_vertex(int vertex) {
    adjacency_list[vertex]; // Create an empty vector if it doesn't exist
}

// Add an edge between two vertices
void Graph::add_edge(int vertex1, int vertex2) {
    adjacency_list[vertex1].push_back(vertex2);
    adjacency_list[vertex2].push_back(vertex1); // For undirected graph
}

// Get adjacency list of the graph
std::unordered_map<int, std::vector<int>> Graph::get_adjacency_list() const {
    return adjacency_list;
}

// Serialize the graph to JSON
json Graph::to_json() const {
    json j;
    for (const auto& pair : adjacency_list) {
        j[std::to_string(pair.first)] = pair.second;
    }
    return j;
}
