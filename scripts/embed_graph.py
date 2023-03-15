'''Build Graph'''
# https://github.com/AnacletoLAB/grape/blob/main/tutorials/Loading_a_Graph_in_Ensmallen.ipynb
from grape import Graph
import os

data_dir = '../data'
output_dir = '../output'
node_path = os.path.join(data_dir, 'node_list.tsv')
edge_path = os.path.join(data_dir, 'edge_list.tsv')

ca_os_graph = Graph.from_csv(# Edges
                             edge_path = edge_path,
                             edge_list_separator = '\t',
                             edge_list_header = True,
                             sources_column = 'head',
                             edge_list_edge_types_column='relation',
                             destinations_column = 'tail',
                             #edge_list_numeric_node_ids=True,
                             weights_column_number=3,
                             
                             # Nodes
                             node_path = node_path,
                             node_list_separator = '\t',
                             node_list_header = True,
                             nodes_column = 'node',
                            
                             # Graph
                             directed = False,
                             name = 'CaProtein-OS',
                             verbose = True)
ca_os_graph.remove_disconnected_nodes()


'''Embed Graph'''
from grape.embedders import TransEEnsmallen, ComplExPyKEEN, FirstOrderLINEEnsmallen
import pandas as pd

graph = ca_os_graph
transE = True
complEx = False
firstline = True

# TransE
if transE == True:
   model = TransEEnsmallen()
   transe_embedding = model.fit_transform(graph)
   transe_node_emb = transe_embedding.get_node_embedding_from_index(0)
   transe_node_emb.to_csv(os.path.join(output_dir, 'TransE_embedding.csv'))

# ComplEx
if complEx == True:
   model = ComplExPyKEEN(can_use_edge_weights=True)
   complex_embedding = model.fit_transform(graph)
   complex_node_emb = complex_embedding.get_node_embedding_from_index(0)
   complex_node_emb.to_csv(os.path.join(output_dir, 'ComplEx_embedding.csv'))

# First Order LINE
if firstline == True:
   model = FirstOrderLINEEnsmallen()
   fline_embedding = model.fit_transform(graph)
   fline_node_emb = fline_embedding.get_node_embedding_from_index(0)
   fline_node_emb.to_csv(os.path.join(output_dir, 'fline_embedding.csv'))
 
