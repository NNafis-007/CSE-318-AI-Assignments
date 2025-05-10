#include <iostream>
#include <utility>
#include <unordered_set>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <limits>
#include <chrono>
#include "heuristics.hpp"

using namespace std;

int main()
{
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
    Graph *G = new Graph(n);
    for (int i = 0; i < m; ++i)
    {
        int u, v, w;
        in >> u >> v >> w;
        if (!in)
        {
            cerr << "Error: malformed edge at line " << (i + 2) << "\n";
            return 1;
        }
        G->addEdge(u, v, w);
    }
    in.close();

    // seed RNG
    srand((unsigned)time(nullptr));

    // parameters
    auto start_random = chrono::high_resolution_clock::now();

    const int RAND_TRIALS = 100; // for randomized heuristic
    const double ALPHA = 0.5;    // for semi-greedy
    const int GRASP_ITERS = 50;  // GRASP iterations

    // 2) Randomized construction: average cut over RAND_TRIALS
    double avgRand = Randomized_max_cut(G, RAND_TRIALS);
    auto stop_random = chrono::high_resolution_clock::now();
    cout << "Randomized (avg over " << RAND_TRIALS << "): "
         << avgRand << " | time = " << (stop_random - start_random).count() / 1e9 << "s\n";

    // // 3) Greedy construction
    auto start_greedy = chrono::high_resolution_clock::now();
    auto XY = Greedy_max_cut(G);
    double wGreedy = G->calc_cut_weight(XY.first, XY.second);
    auto stop_greedy = chrono::high_resolution_clock::now();
    cout << "Greedy: " << wGreedy << " | time = " << (stop_greedy - start_greedy).count() / 1e9 << "s\n";

    // 4) Semi-greedy construction
    auto start_semi_greedy = chrono::high_resolution_clock::now();
    auto XY_sg = SemiGreedy_max_cut(G, ALPHA);
    double wSemi = G->calc_cut_weight(XY_sg.first, XY_sg.second);
    auto stop_semi_greedy = chrono::high_resolution_clock::now();
    cout << "Semi-greedy (alpha=" << ALPHA << "): " << wSemi << " | time = " << (stop_semi_greedy - start_semi_greedy).count() / 1e9 << "s\n";

    // 5) Random + Local Search
    auto start_random_ls = chrono::high_resolution_clock::now();
    auto XY_random = get_Randomized_max_cuts(G);
    double wR0 = G->calc_cut_weight(XY_random.first, XY_random.second);

    auto XY_improved = LocalSearch(G, move(XY_random.first), move(XY_random.second));
    double wR1 = G->calc_cut_weight(XY_improved.first, XY_improved.second);
    auto stop_random_ls = chrono::high_resolution_clock::now();
    cout << "Random with LS: before=" << wR0 << "  after=" << wR1;
    cout << " | time = " << (stop_random_ls - start_random_ls).count() / 1e9 << "s\n";

    // 6) Full GRASP
    auto start_grasp = chrono::high_resolution_clock::now();
    auto XY_grasp = GRASP_max_cut(G, GRASP_ITERS, ALPHA);
    double wGrasp = G->calc_cut_weight(XY_grasp.first, XY_grasp.second);
    auto stop_grasp = chrono::high_resolution_clock::now();
    cout << "GRASP (iters=" << GRASP_ITERS
         << ", alpha =" << ALPHA << "): " << wGrasp;
    cout << " | time = " << (stop_grasp - start_grasp).count() / 1e9 << "s\n";

    delete G;
    return 0;
}
