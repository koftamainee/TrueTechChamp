#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <string>
#include <unordered_map>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Graph {
public:
    Graph();

    // Add a vertex to the graph
    void add_vertex(int vertex);

    // Add an edge between two vertices
    void add_edge(int vertex1, int vertex2);

    // Get adjacency list of the graph
    std::unordered_map<int, std::vector<int>> get_adjacency_list() const;

    // Serialize the graph to JSON
    json to_json() const;

private:
    std::unordered_map<int, std::vector<int>> adjacency_list;
};

#endif // GRAPH_H
