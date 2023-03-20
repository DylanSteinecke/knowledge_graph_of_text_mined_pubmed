import pandas as pd
import networkx as nx

# Assuming `filename` is the path to your TSV file
filename = '../data/cvd_edge_list.tsv'

import networkx as nx

# read the tsv file into a graph
G = nx.read_weighted_edgelist(filename, delimiter='\t', create_using=nx.DiGraph())

# count the number of connected components
num_connected_components = nx.number_strongly_connected_components(G)

# print the size of the connected components
for component in nx.strongly_connected_components(G):
    print(len(component))
