import networkx as nx
import matplotlib.pyplot as plt


def generate_cayley_tree(k, P):
    """
    Generate a Cayley Tree:
    - The root node has degree k.
    - For non-root nodes, each node generates k-1 children.
    - The tree stops growing after level P (nodes at level P are leaves).
    """
    G = nx.Graph()
    # Add the central (root) node with level 0.
    G.add_node(0, level=0)
    current_level = [0]
    next_node = 1
    # Generate nodes level by level until reaching level P.
    for d in range(1, P + 1):
        new_level = []
        for node in current_level:
            # The root node generates k children, while other nodes generate k-1 children.
            children_count = k if G.nodes[node]['level'] == 0 else k - 1
            for _ in range(children_count):
                G.add_node(next_node, level=d)
                G.add_edge(node, next_node)
                new_level.append(next_node)
                next_node += 1
        current_level = new_level
    return G


def plot_tree(G, k, P):
    """
    Plot the structure of the Cayley Tree.
    """
    pos = nx.spring_layout(G)  # Position nodes using the spring layout
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title(f"Cayley Tree with k={k}, P={P}")
    plt.show()


def plot_degree_distribution(G):
    """
    Compute and plot the degree distribution of the tree.
    The x-axis represents the node degree and the y-axis represents the fraction of nodes with that degree.
    """
    degrees = [deg for _, deg in G.degree()]
    degree_count = {}
    for d in degrees:
        degree_count[d] = degree_count.get(d, 0) + 1
    # Sort the degree values
    x = sorted(degree_count.keys())
    y = [degree_count[d] / G.number_of_nodes() for d in x]

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color='skyblue')
    plt.xlabel("Node Degree")
    plt.ylabel("Fraction of Nodes")
    plt.title("Degree Distribution of the Cayley Tree")
    plt.show()


# Parameters
k = 3  # The root node has degree k; internal nodes have degree k (1 edge to parent + k-1 children)
P = 5  # Depth of the tree, with level P nodes being leaves

# Generate the Cayley tree
G = generate_cayley_tree(k, P)
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# Plot the Cayley tree
plot_tree(G, k, P)

# Plot the degree distribution
plot_degree_distribution(G)
