#include <bits/stdc++.h>
#include "heuristics.hpp"

using namespace std;

string getFileNameWithoutExtension(const string &path)
{
    // Find last '/' (or '\\' for Windows)
    size_t lastSlash = path.find_last_of("/\\");
    // Extract the file name with extension
    string filename = path.substr(lastSlash + 1);

    // Find the last '.' to remove extension
    size_t lastDot = filename.find_last_of('.');
    if (lastDot == string::npos)
        return filename; // No extension found

    string str = filename.substr(0, lastDot);
    for (char &c : str)
    {
        c = toupper(static_cast<unsigned char>(c));
    }

    return str;
}

int main()
{
    const unsigned int FIXED_SEED = 2105007;

    string input_file = "graph_GRASP/set1/g18.rud";
    ifstream in(input_file);
    if (!in)
    {
        cerr << "Error: could not open file '" << input_file << "'\n";
        return 1;
    }

    // Read n, m
    int n, m;
    in >> n >> m;
    if (!in)
    {
        cerr << "Error: invalid header in input file '" << input_file << "'\n";
        return 1;
    }

    // Build the graph
    auto start = chrono::high_resolution_clock::now();
    Graph *G = new Graph(n);
    for (int i = 0; i < m; ++i)
    {
        int u, v, w;
        in >> u >> v >> w;
        if (!in)
        {
            cerr << "Error: malformed edge in file '" << input_file << "'\n";
            delete G;
            continue;
        }
        G->addEdge(u, v, w);
    }
    in.close();
    string filename = getFileNameWithoutExtension(input_file);

    cout << "GRAPH : " << filename << " | n = " << n << " | m = " << m << "\n";

    // Parameters
    const int RAND_TRIALS = 100; // for randomized heuristic
    const double ALPHA = 0.4;    // for semi-greedy
    const int GRASP_ITERS = 10;  // GRASP iterations
    const int LS_ITERS = 10;     // GRASP iterations

    // Randomized construction
    double avgRand = Randomized_max_cut(G, RAND_TRIALS, FIXED_SEED);
    cout << "Randomized Results : " << avgRand << "\n";

    // Greedy construction
    auto XY = Greedy_max_cut(G);
    double wGreedy = G->calc_cut_weight(XY.first, XY.second);
    cout << "Greedy Results : " << wGreedy << "\n";

    // Semi-greedy construction
    auto XY_sg = SemiGreedy_max_cut(G, ALPHA, FIXED_SEED);
    double wSemi = G->calc_cut_weight(XY_sg.first, XY_sg.second);
    cout << "Semi-greedy Results : " << wSemi << "\n";

    // Random Construction + Local Search
    double avg_depth;
    double local_avg;

    for (int k = 0; k < LS_ITERS; k++)
    {
        auto XY_random = get_Randomized_max_cuts(G, FIXED_SEED + k);
        int depth = 0;
        auto XY_improved = LocalSearch(G, move(XY_random.first), move(XY_random.second), depth);
        double wR1 = G->calc_cut_weight(XY_improved.first, XY_improved.second);
        avg_depth += depth;
        local_avg += wR1;
    }
    avg_depth = avg_depth / (float)LS_ITERS;
    local_avg = local_avg / (float)LS_ITERS;
    cout << "Local Search Results (" << LS_ITERS << " iters) : " << local_avg << "\n";

    // Full GRASP
    auto XY_grasp = GRASP_max_cut(G, GRASP_ITERS, ALPHA, FIXED_SEED);
    double wGrasp = G->calc_cut_weight(XY_grasp.first, XY_grasp.second);
    cout << "GRASP Results (" << GRASP_ITERS << " iters) : " << wGrasp << "\n";

    // print results
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    // cout << filename << "," << n << "," << m << "," << avgRand << "," << wGreedy << "," << wSemi << "," << LS_ITERS << "," << local_avg << "," << GRASP_ITERS << "," << wGrasp << "\n";
    cout << "Time taken : " << (duration.count() / (float)1000) << "s\n";
}
