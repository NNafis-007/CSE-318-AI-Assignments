#include<bits/stdc++.h>
using namespace std;

int main(){
    // 1) Open the file
    string input_file = "graph_GRASP/set1/g1.rud";
    ifstream in(input_file);
    if (!in)
    {
        cerr << "Error: could not open file '" << input_file << "'\n";
        return 1;
    }

    // 2) Read n, m
    int n, m;
    in >> n >> m;
    if (!in)
    {
        cerr << "Error: invalid header in input file\n";
        return 1;
    }

    // 3) Build the graph
    for (int i = 0; i < m; ++i)
    {
        int u, v, w;
        in >> u >> v >> w;
        if (!in)
        {
            cerr << "Error: malformed edge at line " << (i + 2) << "\n";
            return 1;
        }
        cout << "From " << u << " -> " << v << ", weight " << w << endl;
    }
    in.close();
}