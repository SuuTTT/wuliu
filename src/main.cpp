#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9+7;
const int MAXN = 500;  // Maximum number of nodes
const int MAXM = 10000;  // Maximum number of edges

struct Edge {
    int from, to, cap, cost;
};

vector<Edge> edges;
vector<int> G[MAXN];
int inq[MAXN];  // Whether the node is in the queue
int d[MAXN];  // Distance
int p[MAXN];  // Previous node on the shortest path
int a[MAXN];  // Minimum flow of the path

// Add an edge to the graph
void AddEdge(int from, int to, int cap, int cost) {
    edges.push_back((Edge){from, to, cap, cost});
    edges.push_back((Edge){to, from, 0, -cost});
    int m = edges.size();
    G[from].push_back(m - 2);
    G[to].push_back(m - 1);
}

// Bellman-Ford algorithm to find the shortest path
bool BellmanFord(int s, int t, int &flow, int &cost) {
    for (int i = 0; i < MAXN; i++) d[i] = INF;
    memset(inq, 0, sizeof(inq));
    d[s] = 0; inq[s] = 1; p[s] = 0; a[s] = INF;

    queue<int> Q;
    Q.push(s);
    while (!Q.empty()) {
        int u = Q.front(); Q.pop();
        inq[u] = 0;
        for (int i = 0; i < G[u].size(); i++) {
            Edge& e = edges[G[u][i]];
            if (e.cap > 0 && d[e.to] > d[u] + e.cost) {
                d[e.to] = d[u] + e.cost;
                p[e.to] = G[u][i];
                a[e.to] = min(a[u], e.cap);
                if (!inq[e.to]) { Q.push(e.to); inq[e.to] = 1; }
            }
        }
    }

    if (d[t] == INF) return false;  // Cannot reach the sink
    flow += a[t];
    cost += d[t] * a[t];
    for (int u = t; u != s; u = edges[p[u]].from) {
        edges[p[u]].cap -= a[t];
        edges[p[u]^1].cap += a[t];
    }

    return true;
}

// Main function to calculate the minimum cost maximum flow
int MinCostMaxFlow(int s, int t, int &cost) {
    int flow = 0; cost = 0;
    while (BellmanFord(s, t, flow, cost));
    return flow;
}

int main() {
    // The nodes 0, 1, 2 are warehouses
    // The nodes 3, 4, 5 are orders
    // The nodes 6 is the source node
    // The node 7 is the sink node
    AddEdge(6, 0, 10, 0);  // Supply from the source to the warehouses
    AddEdge(6, 1, 5, 0);
    AddEdge(6, 2, 5, 0);

    AddEdge(0, 3, 10, 5);  // From warehouse to order
    AddEdge(1, 4, 5, 10);
    AddEdge(2, 5, 5, 15);

    AddEdge(0, 1, 10, 1);  // Between warehouses
    AddEdge(1, 2, 10, 1);

    AddEdge(3, 7, 10, 0);  // Demand from the orders to the sink
    AddEdge(4, 7, 5, 0);
    AddEdge(5, 7, 5, 0);

    int cost;
    int maxFlow = MinCostMaxFlow(6, 7, cost);

    cout << "The maximum flow is " << maxFlow << endl;
    cout << "The minimum cost (maximum transportation time) is " << cost << endl;

    return 0;
}