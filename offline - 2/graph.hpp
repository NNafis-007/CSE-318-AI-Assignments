#include <iostream>
#include <vector>
#include <utility>

using namespace std;

typedef pair<int,int> pi;

class Graph
{
private:
    int V;                              // number of vertices
    vector<vector<pi>> adj; // adjacency list: node -> list of (neighbor, weight)

public:
    // Constructor
    Graph(int vertices)
    {
        V = vertices;
        adj.resize(V + 1);
    }

    // Add an edge (undirected)
    void addEdge(int u, int v, int weight)
    {
        if (u > V || v > V || u <= 0 || v <= 0)
        {
            cerr << "Error: Vertex out of bounds\n";
            return;
        }
        adj[u].emplace_back(v, weight);
        adj[v].emplace_back(u, weight);
    }

    // Print the graph
    void printGraph() const
    {
        for (int i = 1; i <= V; ++i)
        {
            cout << "Node " << i << " -> ";
            for (const auto &edge : adj[i])
            {
                cout << "(" << edge.first << ", w = " << edge.second << ") ";
            }
            cout << endl;
        }
    }

    // Get neighbors of a node
    vector<pi> &getNeighbors(int u)
    {
        if (u <= 0 || u > V)
        {
            throw out_of_range("Vertex out of bounds");
        }
        return adj[u];
    }

    double calc_cut_weight(unordered_set<int> &setA,
                     unordered_set<int> &setB)
    {
        double total = 0.0;
        // For every u in A, look at its neighbors
        for (int u : setA)
        {
            if (u < 1 || u > V)
                throw out_of_range("Vertex in setA out of bounds");
            for (auto &edge : adj[u])
            {
                int v = edge.first;
                int w = edge.second;
                // if v is in B, we have a crossing edge (u,v)

                if (setB.find(v) != setB.end())
                {
                    total += w;
                }
            }
        }
        return total;
    }

    //find max-weight edge
    pi max_weight_edge()
    {
        int max_w = 0;
        int u, v, w;
        for (int i = 1; i <= V; i++)
        {
            for (auto &edge : adj[i])
            {
                if (edge.second > max_w)
                {
                    max_w = edge.second;
                    u = i;
                    v = edge.first;
                    w = edge.second;
                }
            }
        }
        return {u, v};
    }

    // Get number of vertices
    int numVertices()
    {
        return V;
    }
};
