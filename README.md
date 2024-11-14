# Market-Clearing-Prices

This Python file is designed for the market clearance process on bipartite graphs stored in `.gml` format. The tool includes steps for identifying sellers and buyers, calculating payoffs, finding constricted sets, and updating prices to find a perfect match in the market.

## Dependencies

This file requires the following Python libraries:

- `argparse`
- `networkx`
- `matplotlib`

You can install the required dependencies using the following command:


## Features

- **Graph Loading**: Reads a bipartite graph from a `.gml` file.
- **Market Clearance Algorithm**: Iteratively adjusts prices and constructs the graph until a perfect match is found.
- **Payoff Calculation**: Calculates the payoff for buyers based on valuations and seller prices.
- **Perfect Match Check**: Identifies whether a perfect matching exists in the bipartite graph.
- **Price Update**: Adjusts prices of sellers that belong to constricted sets to facilitate a perfect match.
- **Graph Plotting**: Visualizes the market graph, showing buyers, sellers, payoffs, and prices.

## Running from Command-line

`python market_clearance.py <file_path> [OPTIONS]`

### Mandatory Arguments:

- `<file_path>`: Path to the `.gml` file containing the bipartite graph.

### Optional Command-Line Options:

- `--plot`: Generates and displays a final plot of the market clearance process.
- `--interactive`: Displays the output of each step, plotting the graph at each iteration.


## Output

- **Payoff Calculation**: Displays the payoff for each buyer and their preferred seller.
- **Constricted Set Detection**: Prints whether a perfect match is found or indicates the presence of constricted sets.
- **Price Update**: Shows updated prices after each iteration.
- **Graph Plot**: Visualizes the bipartite graph with annotated payoffs and prices for each round (if `--interactive` is used) and the final state (if `--plot` is used).

### Graph Plot Details:

- **Node Colors**: 
  - **Sellers**: Light blue.
  - **Buyers**: Light green.
- **Edge Colors**: Green, indicating the best payoff connections.
- **Node Labels**: Nodes are labeled with their respective payoffs (for buyers) and prices (for sellers).

## Functions Overview

- **`read_graph(input_file)`**: Reads the bipartite graph from a `.gml` file.
- **`init_bipartite_graph(graph)`**: Initializes sellers, buyers, prices, and valuations from the input graph.
- **`calculate_payoffs(buyers, prices, valuations)`**: Computes the payoff for each buyer.
- **`calculates_best_payoffs(buyers, prices, valuations)`**: Finds the best payoffs and the preferred sellers for each buyer.
- **`create_bipartite_graph(sellers, buyers, best_payoffs)`**: Constructs a bipartite graph with edges based on the best payoffs.
- **`is_perfect_match(graph, buyers)`**: Checks for a perfect match in the bipartite graph.
- **`update_prices(graph, sellers, prices, buyers)`**: Updates prices for sellers involved in constricted sets.
- **`plot_bipartite_graph(G, buyers, sellers, payoffs, prices)`**: Visualizes the bipartite graph with payoffs and prices.
- **`market_clearance_algo(graph, interactive=False, plot=False)`**: Main logic for market clearance, iteratively updating prices and checking for a perfect match.
