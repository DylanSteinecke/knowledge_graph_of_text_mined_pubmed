# ca_channel
## Biological Task
To generate knowledge graph embeddings based on text data (i.e., protein occurrences in PubMed articles studying certain topics). Proteins of interest here are calcium channel proteins. Topics of interest here are oxidative stress and cardiovascular disease. 


## Process
### Input files
First, upload the input files into the input/{disease_name} folder for whatever your disease name is (e.g., input/os): 

- textcube_config.json: list of the different categories' names (e.g., cardiovascular diseases)

- textcube_category2pmid.json: list of lists of PubMed IDs (PMID). Each list contains the PMIDs studying that category number. Category 0 is named in the 0th entry of the previous file.  

- metadata_pmid2pcount.json: dictionary of PMIDs to entity found in the PMID (i.e., protein) to the number of times it was found there


### Intermediary files (produced when you prepare the graph)
Then, run the script to create the node and edge files. If your disease is named "os", run this command below.

```
python prepare_graph.py -g 'os'
```

The "-g" flag (i.e., --graph_name) indicates the name of your graph / disease. This command produces the node and edge files:

- {disease_name}_node_list.tsv
- {disease_name}_edge_list.tsv


### Output files (knowledge graph embeddings)
Finally, run the script to generate node embeddings. 

```
python embed_graph.py -g 'os'
```
