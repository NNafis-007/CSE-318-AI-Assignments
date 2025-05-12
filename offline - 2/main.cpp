#include <iostream>
#include <utility>
#include <unordered_set>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <limits>
#include <chrono>
#include <fstream>  // For file operations
#include <dirent.h> // For directory iteration
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
    // Set a fixed seed value for reproducibility
    const unsigned int FIXED_SEED = 2105007;

    string input_folder = "graph_GRASP/set1/";
    ofstream csv_out("results.csv", ios::app); // Append mode
    if (!csv_out)
    {
        cerr << "Error: could not open results.csv for writing\n";
        return 1;
    }

    // Write CSV header if the file is empty
    if (csv_out.tellp() == 0)
    {
        csv_out << "Name,|V|,|E|,Randomized-1,Greedy-1,Semi-Greedy-1,Simple local Iteration,LS Avg Value,GRASP Iterations,GRASP Result\n";
    }

    DIR *dir;
    struct dirent *entry;

    if ((dir = opendir(input_folder.c_str())) == nullptr)
    {
        cerr << "Error: could not open directory '" << input_folder << "'\n";
        return 1;
    }

    while ((entry = readdir(dir)) != nullptr)
    {
        string file_name = entry->d_name;
        if (file_name == "." || file_name == "..")
            continue;

        string input_file = input_folder + file_name;
        ifstream in(input_file);
        if (!in)
        {
            cerr << "Error: could not open file '" << input_file << "'\n";
            continue;
        }

        // Read n, m
        int n, m;
        in >> n >> m;
        if (!in)
        {
            cerr << "Error: invalid header in input file '" << input_file << "'\n";
            continue;
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
        const double ALPHA = 0.4;    // for semi-greedy
        const int GRASP_ITERS = 25;  // GRASP iterations
        const int LS_ITERS = 10;

        // Randomized construction
        double avgRand = Randomized_max_cut(G, RAND_TRIALS, FIXED_SEED);

        // Greedy construction
        auto XY = Greedy_max_cut(G);
        double wGreedy = G->calc_cut_weight(XY.first, XY.second);

        // Semi-greedy construction
        auto XY_sg = SemiGreedy_max_cut(G, ALPHA, FIXED_SEED);
        double wSemi = G->calc_cut_weight(XY_sg.first, XY_sg.second);

        // Random Construction + Local Search
        double local_avg = 0.0;

        for (int k = 0; k < LS_ITERS; k++)
        {
            auto XY_random = get_Randomized_max_cuts(G, FIXED_SEED + k);
            int depth = 0;
            auto XY_improved = LocalSearch(G, move(XY_random.first), move(XY_random.second), depth);
            double wR1 = G->calc_cut_weight(XY_improved.first, XY_improved.second);
            local_avg += wR1;
        }
        local_avg = local_avg / LS_ITERS;

        // Full GRASP
        auto XY_grasp = GRASP_max_cut(G, GRASP_ITERS, ALPHA, FIXED_SEED);
        double wGrasp = G->calc_cut_weight(XY_grasp.first, XY_grasp.second);

        // Write results to CSV
        string filename = getFileNameWithoutExtension(input_file);
        csv_out << filename << "," << n << "," << m << "," << avgRand << "," << wGreedy << "," << wSemi << "," << LS_ITERS << "," << local_avg << "," << GRASP_ITERS << "," << wGrasp << "\n";

        // csv_out << filename << "," << n << "," << m << "," << avgRand << "," << wGreedy << "," << wSemi << "," << wR1 << "," << GRASP_ITERS << "," << wGrasp << "\n";
        auto end = chrono::high_resolution_clock::now();
        auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
        cout << "Processed file: " << filename << " | Time taken: " << (duration.count() / (float)1000) << "s\n";
        delete G;
    }

    closedir(dir);
    csv_out.close();
    return 0;
}
