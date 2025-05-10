#include<bits/stdc++.h>
#include "heuristics.hpp"

using namespace std;

int main() {
    Graph* g = new Graph(4);

    g->addEdge(1,2,3);
    g->addEdge(1,3,2);
    g->addEdge(1,4,1);
    g->addEdge(2,3,4);
    g->addEdge(2,4,5);
    g->addEdge(3,4,2);

    g->printGraph();

    // cout << "Avg cut weight = " << Randomized_max_cut(g, 5) << endl;
    // auto XY = get_Randomized_max_cuts(g);
    // auto X = XY.first;
    // auto Y = XY.second;


    unordered_set<int> X = {1,2,4}; 
    unordered_set<int> Y = {3};
    print_cuts(X, Y);
    cout << "Cut weight : " << g->calc_cut_weight(X, Y) << endl; 

    int max_iter = 5;
    double alpha = 0.5;

    auto XY = GRASP_max_cut(g, max_iter, alpha);
    X = XY.first;
    Y = XY.second;
    print_cuts(X, Y);
    cout << "Cut weight : " << g->calc_cut_weight(X, Y) << endl; 

    return 0;


}
