"""
We have two data files in the same directory:

1) global-cities.dat
   Each line is in the format: <CODE>|<NODE_ID>|<CITY_NAME>

   - <NODE_ID> is the numeric ID of the node.
   - We will use the numeric ID as the node identifier in our graph.
   - <CITY_NAME> will be stored as a node attribute.

2) global-net.dat
   Each line contains two numeric IDs representing an undirected edge between those nodes.

"""

import networkx as nx
import matplotlib.pyplot as plt


def build_graph(cities_file='global-cities.dat', network_file='global-net.dat'):
    """
    Build and return an undirected graph from the air traffic network data.

    :param cities_file:    Path to the 'global-cities.dat' file
    :param network_file:   Path to the 'global-net.dat' file
    :return:               A NetworkX undirected Graph (G)
    """
    G = nx.Graph()

    # 1) Parse global-cities.dat: add each numeric node ID and store city code and city name
    with open(cities_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 3:
                code = parts[0]  # e.g. "CBR"
                node_id = parts[1]  # numeric node ID
                city_name = parts[2]  # e.g. "Canberra"

                # Store both code and city as attributes
                G.add_node(node_id, code=code, city=city_name)

    with open(network_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                node1, node2 = parts
                G.add_edge(node1, node2)

    return G


def solve_problem2_q1(G):
    """
    Problem2 (Q1):
      - Print how many nodes and edges are in the undirected graph G.
    """
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print("=== Problem2 (Q1) ===")
    print("Number of nodes (undirected):", num_nodes)
    print("Number of edges (undirected):", num_edges)


def solve_problem2_q2(G):
    """
    Problem2 (Q2):
      - How many connected components are in this graph?
      - How many nodes and edges does the largest connected component contain?
    """
    # 1) Number of connected components in an undirected graph
    num_components = nx.number_connected_components(G)

    # 2) Identify the largest connected component (by node count)
    #    connected_components(G) returns a generator of node sets
    largest_cc_nodeset = max(nx.connected_components(G), key=len)

    # Create the subgraph for the largest CC
    largest_cc_subgraph = G.subgraph(largest_cc_nodeset)
    largest_cc_num_nodes = largest_cc_subgraph.number_of_nodes()
    largest_cc_num_edges = largest_cc_subgraph.number_of_edges()

    # Print the results
    print("=== Problem2 (Q2) ===")
    print("Number of connected components:", num_components)
    print("Largest connected component:")
    print("   Nodes:", largest_cc_num_nodes)
    print("   Edges:", largest_cc_num_edges)


def solve_problem2_q3(G):
    """
    Problem2 (Q3):
      - Denote the largest component as G_largest.
      - List the top 10 nodes in G_largest that have the highest degree.
      - Print the city/airport name and the degree (not the node ID).
    """

    # 1) Identify the largest connected component
    #    connected_components(G) returns sets of nodes. Pick the set with the largest length.
    largest_cc_nodeset = max(nx.connected_components(G), key=len)
    # Create a subgraph for the largest connected component
    G_largest = G.subgraph(largest_cc_nodeset)

    # 2) Compute the degree of each node in G_largest
    #    G_largest.degree() returns (node, degree)
    node_degree_pairs = list(G_largest.degree())

    # 3) Sort by degree in descending order
    #    x[1] is the degree, so we sort by that, reversed.
    node_degree_pairs.sort(key=lambda x: x[1], reverse=True)

    # 4) Take the top 10
    top_10 = node_degree_pairs[:10]

    # 5) Print results
    #    We specifically need city names, not node IDs.
    #    The city name is stored under the 'city' attribute: G_largest.nodes[node_id]['city'].
    print("=== Problem2 (Q3) ===")
    print("Top 10 nodes in the largest component by degree:")
    for node_id, deg in top_10:
        city_name = G_largest.nodes[node_id]['city']
        print(f"  - City/Airport: {city_name}, Degree: {deg}")


def solve_problem2_q4(G):
    """
    Problem2 (Q4):
      - Plot the degree distribution of the largest connected component G_largest.
      - Each data point (x, y) where x is a positive integer (the degree),
        and y is the fraction of nodes in the network whose degree equals x.
      - Also plot the degree distribution on a log-log scale (base 10).
      - Restrict the range of x between the min and max degree, and ignore any points with y=0.
    """

    # 1) Identify the largest connected component
    largest_cc_nodeset = max(nx.connected_components(G), key=len)
    G_largest = G.subgraph(largest_cc_nodeset)

    # 2) Compute the degree of each node in G_largest
    degrees = [d for _, d in G_largest.degree()]

    # 3) Build a frequency dictionary: degree -> how many nodes have this degree
    from collections import Counter
    degree_counts = Counter(degrees)

    # total number of nodes in G_largest
    n_nodes = G_largest.number_of_nodes()

    # 4) Convert to (x, y) pairs where
    #    x = degree,
    #    y = fraction = count_of_nodes_with_that_degree / total_nodes
    #    Then filter out any with 0 (normally won't appear anyway, but for safety).
    x_vals = []
    y_vals = []
    for deg in sorted(degree_counts.keys()):
        count = degree_counts[deg]
        fraction = count / n_nodes
        if fraction > 0:
            x_vals.append(deg)
            y_vals.append(fraction)

    # 5) Plot in normal scale
    plt.figure()  # first figure: normal scale
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', label='Degree Distribution',markersize=3, alpha=0.8)
    plt.title("Degree Distribution (Largest Component) - Linear Scale")
    plt.xlabel("Degree (x)")
    plt.ylabel("Fraction of Nodes (y)")
    plt.legend()
    plt.grid(True)
    plt.show()  # Show the first plot

    # 6) Plot in log-log scale
    #    base 10 for both x and y axes
    plt.figure()  # second figure: log-log scale
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', label='Degree Distribution',markersize=3, alpha=0.8)
    plt.title("Degree Distribution (Largest Component) - Log-Log Scale")
    plt.xlabel("Degree (log10)")
    plt.ylabel("Fraction of Nodes (log10)")
    plt.xscale('log', base=10)
    plt.yscale('log', base=10)
    plt.legend()
    plt.grid(True)
    plt.show()  # Show the second plot


def solve_problem2_q5(G):
    """
    Problem2 (Q5):
      - What is the (unweighted) diameter of the giant component G_largest?
      - List a longest (unweighted) shortest path between two cities in G_largest,
        printing city/airport names (not node IDs), whose distance equals the diameter.

    Steps:
      1) Extract the largest connected component and create G_largest.
      2) Use nx.diameter(G_largest) to find the unweighted diameter.
      3) Use nx.periphery(G_largest) to get all nodes whose eccentricity equals the diameter.
      4) Pick one of those periphery nodes (p0) and run a BFS or single_source_shortest_path
         to find which node in G_largest is at distance = diameter (p1).
      5) Retrieve the actual shortest path between p0 and p1 using nx.shortest_path.
      6) Print city names for each node in that path.
    """

    # 1) Identify the largest connected component
    largest_cc_nodeset = max(nx.connected_components(G), key=len)
    G_largest = G.subgraph(largest_cc_nodeset).copy()

    # 2) Compute the unweighted diameter of G_largest
    diameter = nx.diameter(G_largest)

    # 3) Get all nodes in the periphery (distance to their farthest node = diameter)
    #    nx.periphery(G_largest) returns a list of such nodes.
    periphery_nodes = nx.periphery(G_largest)

    # 4) Pick one of these periphery nodes, say p0
    p0 = periphery_nodes[0]

    # 5) Use BFS (or single_source_shortest_path_length) from p0 to find the node p1
    #    that is at distance = diameter from p0
    dist_from_p0 = nx.single_source_shortest_path_length(G_largest, p0)
    # Find p1 whose distance from p0 is exactly 'diameter'
    candidates = [n for n, dist in dist_from_p0.items() if dist == diameter]
    if not candidates:
        # If for some reason we can't find any node at distance = diameter,
        # fallback approach: it should not happen theoretically, but just in case:
        print("No node found at distance = diameter. Something unexpected occurred.")
        return

    p1 = candidates[0]  # take the first one

    # 6) Retrieve the actual shortest path from p0 to p1
    path_nodes = nx.shortest_path(G_largest, p0, p1)

    # Convert node IDs to city/airport names
    path_cities = [G_largest.nodes[node]['city'] for node in path_nodes]

    # Print results
    print("=== Problem2 (Q5) ===")
    print("Diameter of the giant component:", diameter)
    print("One longest shortest path between two cities (by city name):")
    print(" -> ".join(path_cities))


def solve_problem2_q6(G):
    """
    Problem2 (Q6):
      - Find the smallest number of flights from Canberra (CBR) to Cape Town (CPT).
      - List the route (airports) by printing the city/airport names only.

    Steps:
      1) Find the node whose 'code' == "CBR" (start) and the node whose 'code' == "CPT" (target).
      2) Compute the shortest path (unweighted) in the undirected graph.
      3) The smallest number of flights = (length of path in terms of nodes) - 1.
      4) Print the sequence of city/airport names along that path.
    """


    # 1) Identify the node IDs for Canberra (CBR) and Cape Town (CPT)
    start_node = None
    end_node = None

    for node_id, attrs in G.nodes(data=True):
        if attrs.get('code') == "CBR":
            start_node = node_id
        elif attrs.get('code') == "CPT":
            end_node = node_id

    if start_node is None or end_node is None:
        print("Could not find 'CBR' or 'CPT' in the graph. Check data or code attribute.")
        return

    # 2) Compute shortest path from start_node to end_node (unweighted)
    try:
        path_nodes = nx.shortest_path(G, source=start_node, target=end_node)
    except nx.NetworkXNoPath:
        print("No path found between Canberra (CBR) and Cape Town (CPT). They may be in different components.")
        return

    # 3) Number of flights = number_of_edges = len(path_nodes) - 1
    num_flights = len(path_nodes) - 1

    # 4) Print the route by city names only
    path_cities = [G.nodes[n]['city'] for n in path_nodes]

    print("=== Problem2 (Q6) ===")
    print(f"Smallest number of flights from Canberra (CBR) to Cape Town (CPT): {num_flights}")
    print("Route (city/airport names only):")
    print(" -> ".join(path_cities))


def solve_problem2_q7(G):
    """
    Problem2 (Q7):
      - Which airport/city in the largest component G_largest has the highest betweenness?
      - List the top 10 cities with their betweenness value.

    Steps:
      1) Extract the largest connected component (G_largest).
      2) Compute betweenness centrality for all nodes in G_largest.
      3) Sort by betweenness in descending order.
      4) Print the top 10 nodes, with their city names and betweenness scores.
    """


    # 1) Identify the largest connected component
    largest_cc_nodeset = max(nx.connected_components(G), key=len)
    G_largest = G.subgraph(largest_cc_nodeset).copy()

    # 2) Compute betweenness centrality
    #    Note: For large graphs, this might take time.
    betweenness_dict = nx.betweenness_centrality(G_largest)

    # 3) Sort nodes by betweenness (descending)
    sorted_by_bc = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)

    # 4) Take top 10
    top_10 = sorted_by_bc[:10]

    print("=== Problem2 (Q7) ===")
    print("Top 10 airports/cities by betweenness (largest connected component):")
    for node_id, bc_value in top_10:
        city_name = G_largest.nodes[node_id]['city']
        print(f"  - City : {city_name}, Betweenness: {bc_value:.6f}")


def main():
    """
    Main entry point: build the graph once, then solve Q1 and Q2.
    """
    # Build the graph from the .dat files
    G = build_graph()

    # Q1: Print number of nodes and edges
    solve_problem2_q1(G)

    # Q2: Connected components info
    solve_problem2_q2(G)

    # Q3: top 10 nodes in G having the highest degree
    solve_problem2_q3(G)

    # Q4: Plot degree distribution
    solve_problem2_q4(G)

    # Q5: List a longest (unweighted) shortest path between two cities
    solve_problem2_q5(G)

    # Q6: The smallest number of flights from Canberra (CBR) to Cape Town (CPT)
    solve_problem2_q6(G)

    # Q7: Top10 cities have the largest betweeness
    solve_problem2_q7(G)


if __name__ == '__main__':
    main()

