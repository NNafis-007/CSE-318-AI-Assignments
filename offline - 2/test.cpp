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

    string input_file = "graph_GRASP/set1/g1.rud";
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

    // Parameters
    const int RAND_TRIALS = 100; // for randomized heuristic
    const double ALPHA = 0.5;    // for semi-greedy
    const int GRASP_ITERS = 10;  // GRASP iterations

    // Randomized construction
    double avgRand = Randomized_max_cut(G, RAND_TRIALS, FIXED_SEED);

    // Greedy construction
    auto XY = Greedy_max_cut(G);
    double wGreedy = G->calc_cut_weight(XY.first, XY.second);

    // Semi-greedy construction
    auto XY_sg = SemiGreedy_max_cut(G, ALPHA, FIXED_SEED);
    double wSemi = G->calc_cut_weight(XY_sg.first, XY_sg.second);

    // Random + Local Search
    auto XY_random = get_Randomized_max_cuts(G, FIXED_SEED);
    double wR0 = G->calc_cut_weight(XY_random.first, XY_random.second);
    int num_iters_LS = 0;
    auto XY_improved = LocalSearch(G, move(XY_random.first), move(XY_random.second), num_iters_LS);
    double wR1 = G->calc_cut_weight(XY_improved.first, XY_improved.second);

    // Full GRASP
    auto XY_grasp = GRASP_max_cut(G, GRASP_ITERS, ALPHA, FIXED_SEED);
    double wGrasp = G->calc_cut_weight(XY_grasp.first, XY_grasp.second);

    // Write results to CSV
    string filename = getFileNameWithoutExtension(input_file);
    cout << filename << "," << n << "," << m << "," << avgRand << "," << wGreedy << "," << wSemi << "," << num_iters_LS << ","  << wR1 << "," << GRASP_ITERS << "," << wGrasp << "\n";
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "Processed file: " << filename << " | Time taken: " << (duration.count() / (float)1000) << " s\n";
}
