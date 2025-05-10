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
    while (!rem_vertices.empty())
    {
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
        //calculate threshold
        double threshold = w_min + (alpha * (w_max - w_min));

        //construct RCL
        vector<int> RCL;
        for(auto candidate : rem_vertices){
            if(greedy_fn_vals[candidate] >= threshold){
                RCL.push_back(candidate);
            }   
        }

        //choose a random vertex from RCL
        int rand_index = rand() % RCL.size();
        int chosen = RCL[rand_index];

        if(sigma_X_vals[chosen] > sigma_Y_vals[chosen]){
            X.insert(chosen);
        }
        else{
            Y.insert(chosen);
        }
        rem_vertices.erase(rem_vertices.find(chosen));
        
    }

    return {X, Y};    
}