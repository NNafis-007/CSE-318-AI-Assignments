#include <bits/stdc++.h>
#include "graph.hpp"
using namespace std;

void print_cuts(unordered_set<int> &X, unordered_set<int> &Y)
{
    cout << "X partition : {";
    for (auto x : X)
    {
        cout << x << ",";
    }
    cout << "}" << endl;

    cout << "Y partition : {";
    for (auto y : Y)
    {
        cout << y << ",";
    }
    cout << "}" << endl;
}

pair<unordered_set<int>, unordered_set<int>>
get_Randomized_max_cuts(Graph *G)
{

    // generate a random number
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);

    double total_cut_w = 0;
    int n_vertices = G->numVertices();

    unordered_set<int> X_part = {};
    unordered_set<int> Y_part = {};
    for (int j = 1; j <= n_vertices; j++)
    {
        double prob = dis(gen);
        if (prob >= 0.5)
            X_part.insert(j);
        else
            Y_part.insert(j);
    }
    return {X_part, Y_part};
}

double Randomized_max_cut(Graph *G, int n)
{

    // generate a random number
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);

    double total_cut_w = 0;
    int n_vertices = G->numVertices();
    for (int i = 0; i < n; i++)
    {
        unordered_set<int> X_part = {};
        unordered_set<int> Y_part = {};
        for (int j = 1; j <= n_vertices; j++)
        {
            double prob = dis(gen);
            if (prob >= 0.5)
                X_part.insert(j);
            else
                Y_part.insert(j);
        }
        double cut_wei = G->calc_cut_weight(X_part, Y_part);
        total_cut_w += cut_wei;
    }
    double avg_cut_wei = (total_cut_w) / n;
    return avg_cut_wei;
}

pair<unordered_set<int>, unordered_set<int>>
Greedy_max_cut(Graph *G)
{
    unordered_set<int> X = {};
    unordered_set<int> Y = {};
    pi max_w_edge = G->max_weight_edge();
    int u = max_w_edge.first;
    int v = max_w_edge.second;
    int n_vertices = G->numVertices();
    X.insert(u);
    Y.insert(v);
    unordered_set<int> rem_vertices = {};

    for (int i = 1; i <= n_vertices; i++)
    {
        if (i != u && i != v)
        {
            rem_vertices.insert(i);
        }
    }

    for (int z : rem_vertices)
    {
        vector<pi> &z_neighbours = G->getNeighbors(z);
        double w_X = 0;
        double w_Y = 0;

        for (auto &edge : z_neighbours)
        {
            int to = edge.first;
            int w = edge.second;
            if (X.find(to) != X.end())
            {
                w_Y += w;
            }
            if (Y.find(to) != Y.end())
            {
                w_X += w;
            }
        }
        if (w_X > w_Y)
        {
            X.insert(z);
        }
        else
        {
            Y.insert(z);
        }
    }
    return {X, Y};
}

pair<unordered_set<int>, unordered_set<int>>
SemiGreedy_max_cut(Graph *G, double alpha)
{
    // for random selection from RCL
    static bool seeded = false;
    if (!seeded)
    {
        srand((unsigned)time(nullptr));
        seeded = true;
    }

    int n_vertices = G->numVertices();
    unordered_set<int> X = {};
    unordered_set<int> Y = {};
    pi max_w_edge = G->max_weight_edge();
    int u = max_w_edge.first;
    int v = max_w_edge.second;
    X.insert(u);
    Y.insert(v);
    unordered_set<int> rem_vertices = {};

    for (int i = 1; i <= n_vertices; i++)
    {
        if (i != u && i != v)
        {
            rem_vertices.insert(i);
        }
    }

    double w_max = INT32_MIN;
    double w_min = INT32_MAX;
    // int iter = 1;
    while (!rem_vertices.empty())
    {
        // if (iter % 100 == 0)
        // {
        //     cout << "in loop, iteration no : " << iter << endl;
        // }
        // iter++;
        unordered_map<int, double> greedy_fn_vals;
        unordered_map<int, double> sigma_X_vals;
        unordered_map<int, double> sigma_Y_vals;
        for (int z : rem_vertices)
        {
            vector<pi> &z_neighbours = G->getNeighbors(z);
            double sigma_X = 0;
            double sigma_Y = 0;

            // evaluate the greedy function value and update w_max and w_min
            for (auto &edge : z_neighbours)
            {
                int to = edge.first;
                int w = edge.second;

                // has edge with X
                if (X.find(to) != X.end())
                {
                    sigma_X += w;
                }

                // has edge with Y
                if (Y.find(to) != Y.end())
                {
                    sigma_Y += w;
                }
            }
            greedy_fn_vals[z] = max(sigma_X, sigma_Y);
            sigma_X_vals[z] = sigma_Y;
            sigma_Y_vals[z] = sigma_X;

            w_max = max(w_max, max(sigma_X, sigma_Y));
            w_min = min(w_min, min(sigma_X, sigma_Y));
        }
        // calculate threshold
        double threshold = w_min + (alpha * (w_max - w_min));

        // construct RCL
        vector<int> RCL;
        for (auto candidate : rem_vertices)
        {
            if (greedy_fn_vals[candidate] >= threshold)
            {
                RCL.push_back(candidate);
            }
        }

        // choose a random vertex from RCL
        int chosen;
        if (RCL.size() == 0)
        {
            alpha = alpha * 0.9; // reduce alpha
            int rand_index = rand() % rem_vertices.size();
            auto it = rem_vertices.begin();
            advance(it, rand_index); // move iterator forward by random_index

            chosen = *it; // get the value at that iterator
        }
        else
        {
            int rand_index = rand() % RCL.size();
            chosen = RCL[rand_index];
        }

        if (sigma_X_vals[chosen] > sigma_Y_vals[chosen])
        {
            X.insert(chosen);
        }
        else
        {
            Y.insert(chosen);
        }
        rem_vertices.erase(rem_vertices.find(chosen));
    }

    return {X, Y};
}

pair<unordered_set<int>, unordered_set<int>>
LocalSearch(Graph *G,
            unordered_set<int> X,
            unordered_set<int> Y)
{
    bool improvement = true;

    // Repeat until we can no longer improve
    while (improvement)
    {
        improvement = false;
        double bestDelta = 0.0;
        int best_vertex = -1;
        bool toX = false; // whether to move to X set

        // checking if v in X, should be in Y
        for (int v : X)
        {
            double sumToX = 0, sumToY = 0;

            // Calculate contribution sums
            for (auto &e : G->getNeighbors(v))
            {
                int u = e.first, w = e.second;
                if (X.count(u))
                    sumToX += w; // edge to same side X
                else
                    sumToY += w; // edge to opposite side Y
            }

            // Gain = new cut edges (to X) minus old cut edges (to Y)
            double delta = sumToX - sumToY;
            if (delta > bestDelta)
            {
                bestDelta = delta;
                best_vertex = v;
                toX = false; // we’ll move v → Y
            }
        }

        // checking if v in Y, should be in X
        for (int v : Y)
        {
            double sumToX = 0, sumToY = 0;

            for (auto &e : G->getNeighbors(v))
            {
                int u = e.first, w = e.second;
                if (X.count(u))
                    sumToX += w;
                else
                    sumToY += w;
            }

            double delta = sumToY - sumToX;
            if (delta > bestDelta)
            {
                bestDelta = delta;
                best_vertex = v;
                toX = true; // we’ll move v → X
            }
        }

        // If the best found move gives a positive gain, DO ITTT!!!
        if (bestDelta > 0 && best_vertex != -1)
        {
            improvement = true;
            if (toX)
            {
                // move best_vertex from Y to X
                Y.erase(best_vertex);
                X.insert(best_vertex);
            }
            else
            {
                // move best_vertex from X to Y
                X.erase(best_vertex);
                Y.insert(best_vertex);
            }
        }
    }

    // Return the locally optimized partition
    return make_pair(move(X), move(Y));
}

// GRASP Algo: runs maxIters times
pair<unordered_set<int>, unordered_set<int>>
GRASP_max_cut(Graph *G, int maxIters, double alpha)
{
    // Seed rand once
    static bool seeded = false;
    if (!seeded)
    {
        srand((unsigned)time(nullptr));
        seeded = true;
    }

    unordered_set<int> bestX, bestY;
    double bestWeight = INT32_MIN;

    for (int i = 1; i <= maxIters; ++i)
    {
        // FIRST, -> semi-greedy construction (parameter α)
        auto XY_init = SemiGreedy_max_cut(G, alpha);

        // SECOND -> local-search improvement
        auto XY_improved = LocalSearch(G, move(XY_init.first), move(XY_init.second));
        auto X1 = XY_improved.first;
        auto Y1 = XY_improved.second;

        // Evaluate its weight
        double w = G->calc_cut_weight(X1, Y1);

        // update the best soln
        if (i == 1 || w > bestWeight)
        {
            bestWeight = w;
            bestX = move(X1);
            bestY = move(Y1);
        }
    }

    // Finally returns the best cut found.
    return {move(bestX), move(bestY)};
}
