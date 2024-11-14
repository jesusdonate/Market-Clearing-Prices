import networkx as nx
import matplotlib.pyplot as plt
import argparse
from itertools import chain, combinations


# Function to read a .gml graph file
def read_graph(input_file) -> nx.Graph:
    print(f"Loading graph from {input_file}...")
    try:
        G = nx.read_gml(input_file)
        print(f"Returning {G}")
        return G
    except nx.NetworkXError as e:
        # Handle error if the file cannot be read as a .gml
        print(f"Could not read .gml file from {input_file}...")
        print(e)
    except FileNotFoundError as e:
        # Handle error if the file is not found
        print(f"Could not read .gml file from {input_file}...")
        print(e)


# Function to initialize the bipartite graph with sellers, buyers, prices, and valuations
def init_bipartite_graph(graph: nx.Graph):
    try:
        # Extract seller nodes (bipartite attribute = 0)
        sellers = [node for node, data in graph.nodes(data=True) if data['bipartite'] == 0]
        # Extract buyer nodes (bipartite attribute = 1)
        buyers = [node for node, data in graph.nodes(data=True) if data['bipartite'] == 1]
        # Extract prices for sellers
        prices = [data["price"] for node, data in graph.nodes(data=True) if data['bipartite'] == 0]
        print("sellers:", sellers)
        print("buyers:", buyers)
        print("prices:", prices)

        # Create a list to store valuations for each buyer
        valuations = []

        # Loop through each buyer to find the valuations associated with sellers
        for b in range(len(buyers)):
            valuations.append({})
            for seller, buyer, data in graph.edges(data=True):
                # Check if the edge is connected to the current buyer and store the valuation
                if buyer == buyers[b]:
                    valuations[b][seller] = data["valuation"]
        print("Valuations:", valuations)
        return sellers, buyers, prices, valuations
    except KeyError as e:
        # Handle missing data attributes in the graph
        print(f"Error: You must have a data attribute called {e} for your nodes in your .gml file.")


# Function to calculate payoffs for each buyer
def calculate_payoffs(buyers, prices, valuations):
    payoffs = []
    for b in range(len(buyers)):
        payoffs.append({})
        # Calculate the payoff for each seller (valuation - price)
        for seller, valuation in valuations[b].items():
            try:
                payoffs[b][seller] = valuation - prices[int(seller)]
            except TypeError as e:
                # Handle type errors if node IDs are not integers
                print("Error: The id of the nodes can only be integers.")
    print("Payoffs: ", payoffs)
    return payoffs


# Function to find the best payoffs for each buyer
def calculates_best_payoffs(buyers, prices, valuations):
    payoffs = calculate_payoffs(buyers, prices, valuations)
    best_payoffs = []
    for b in range(len(buyers)):
        best_payoffs.append({})
        best_payoff = float('-inf')
        best_sellers = []
        # Determine the highest payoff for each buyer
        for seller, payoff in payoffs[b].items():
            if payoff > best_payoff:
                best_payoff = payoff
                best_sellers = [seller]
            elif payoff == best_payoff:
                best_sellers.append(seller)
        best_payoffs[b][best_payoff] = best_sellers
    print("Best payoffs: ", best_payoffs)
    return best_payoffs


# Function to create a bipartite graph based on the best payoffs
def create_bipartite_graph(sellers, buyers, best_payoffs):
    graph = nx.Graph()
    # Add seller and buyer nodes with bipartite attributes
    graph.add_nodes_from(sellers, bipartite=0)
    graph.add_nodes_from(buyers, bipartite=1)
    # Add edges based on the best payoffs for buyers
    for i, buyer in enumerate(buyers):
        for payoff, sellers_with_best_payoff in best_payoffs[i].items():
            for seller in sellers_with_best_payoff:
                graph.add_edge(buyer, seller)
    return graph


# Function to generate all non-empty subsets of a set of nodes
def all_subsets(nodes):
    return chain.from_iterable(combinations(nodes, r) for r in range(1, len(nodes) + 1))


# Function to check if there is a perfect match in the graph
def is_perfect_match(graph, buyers):
    for subset in all_subsets(buyers):
        subset = set(subset)
        # Find the neighborhood of the subset
        neighborhood = set(chain.from_iterable(graph.neighbors(node) for node in subset))
        # Check if the subset is constricted
        if len(neighborhood) < len(subset):
            print("No Perfect Match")
            return False
    print("Perfect Match Found")
    return True


# Function to update the prices of sellers in constricted sets
def update_prices(graph, sellers, prices, buyers):
    sellers_to_increment = set()
    for subset in all_subsets(buyers):
        subset = set(subset)
        # Find the neighborhood of the subset
        neighborhood = set(chain.from_iterable(graph.neighbors(node) for node in subset))
        # Identify constricted sets
        if len(neighborhood) < len(subset):
            sellers_to_increment.update(neighborhood)
    # Increment prices of sellers in constricted sets
    for s in range(len(sellers)):
        if sellers[s] in sellers_to_increment:
            prices[s] += 1
    print("Updated prices:", prices)
    return prices


# Placeholder function to create a bipartite random graph
def bipartite_random_graph():
    pass


# Function to plot the bipartite graph with payoffs and prices
def plot_bipartite_graph(G: nx.Graph, buyers, sellers, payoffs, prices):
    print("Plotting graph...")
    try:
        pos = nx.bipartite_layout(G, sellers)
        # Draw the graph with node and edge customization
        nx.draw(G, pos, with_labels=True,
                node_color=["lightblue" if node in sellers else "lightgreen" for node in G.nodes()],
                edge_color="green", font_weight='bold')
        # Annotate buyer nodes with their payoffs
        for i, buyer in enumerate(buyers):
            if i < len(payoffs):
                payoff_values = list(payoffs[i].values())
                payoff_text = f"Payoffs: {payoff_values}"
                plt.text(pos[buyer][0] - 0.1, pos[buyer][1] + 0.07, payoff_text, fontsize=7, color='black')
        # Annotate seller nodes with their prices
        for idx, seller in enumerate(sellers):
            if idx < len(prices):
                price_text = f"Price: {prices[idx]}"
                plt.text(pos[seller][0] - 0.06, pos[seller][1] - 0.09, price_text, fontsize=7, color='red')
        plt.show()
    except KeyError as e:
        # Handle missing data attributes for nodes
        print(f"Error: You must have a data attribute called {e} for your nodes in your .gml file.")


# Main function to run the market clearance algorithm
def market_clearance_algo(graph: nx.Graph, interactive=False, plot=False):
    sellers, buyers, prices, valuations = init_bipartite_graph(graph)
    best_payoffs = calculates_best_payoffs(buyers, prices, valuations)
    new_graph = create_bipartite_graph(sellers, buyers, best_payoffs)
    # Plot the graph if interactive mode is enabled
    if interactive:
        plot_bipartite_graph(new_graph, buyers, sellers, calculate_payoffs(buyers, prices, valuations), prices)
    # Loop until a perfect match is found
    while not is_perfect_match(new_graph, buyers):
        prices = update_prices(new_graph, sellers, prices, buyers)
        best_payoffs = calculates_best_payoffs(buyers, prices, valuations)
        new_graph = create_bipartite_graph(sellers, buyers, best_payoffs)
        # Plot each iteration if interactive mode is enabled
        if interactive:
            plot_bipartite_graph(new_graph, buyers, sellers, calculate_payoffs(buyers, prices, valuations), prices)
    # Plot the final result if plot option is enabled
    if plot:
        plot_bipartite_graph(new_graph, buyers, sellers, calculate_payoffs(buyers, prices, valuations), prices)


# Main function to parse arguments and execute the algorithm
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help="Path to .gml file")
    parser.add_argument('--plot', action="store_true", help="Plot the graph with market strategy.")
    parser.add_argument('--interactive', action="store_true", help="Shows the output of every round graph")
    args = parser.parse_args()
    graph = read_graph(args.file_path)
    if graph is not None:
        market_clearance_algo(graph, args.interactive, args.plot)


# Run the script when executed as the main program
if __name__ == "__main__":
    main()
