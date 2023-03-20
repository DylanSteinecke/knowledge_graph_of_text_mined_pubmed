import json
import os
import csv
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--graph_name', type = str)
args = parser.parse_args()

graph_name = args.graph_name

input_dir = os.path.join('../input', graph_name)
pmid_to_protein_inf = os.path.join(input_dir, 'metadata_pmid2pcount.json')
category_to_pmid_inf = os.path.join(input_dir, 'textcube_category2pmid.json')
category_names_inf = os.path.join(input_dir, 'textcube_config.json')

data_dir = '../data'
edge_outf = f'{graph_name}_edge_list.tsv' #args.edge_file
node_outf = f'{graph_name}_node_list.tsv' #args.node_file
edge_path = os.path.join(data_dir, edge_outf)
node_path = os.path.join(data_dir, node_outf)


'''Input data'''
# Protein-to-PMID
pmid_to_protein_to_count = json.load(open(pmid_to_protein_inf))
pmids_in_cats = json.load(open(category_to_pmid_inf))
cat_names = json.load(open(category_names_inf))

# TopicName-to-PMID
cat_to_pmids = dict()
for num, pmid_list in enumerate(pmids_in_cats):
    cat_name = cat_names[num]
    cat_to_pmids[cat_name] = pmid_list
    
# Proteins'''
all_proteins = set()
for proteins_to_counts in pmid_to_protein_to_count.values():
    for protein in proteins_to_counts:
        all_proteins.add(protein)
all_proteins = list(all_proteins)




'''Write in graph-ready csv format'''
### Edges
with open(edge_path,'w') as fout:
    edge_writer = csv.writer(fout, delimiter = '\t')
    edge_writer.writerow(['head', 'relation', 'tail', 'weight'])

    # MeSH 'Tree'
    for cat in cat_to_pmids:
        edge_writer.writerow([str(f"MeSH:{graph_name}_Root"), '-parent_of->', 'MeSH:'+cat, '1'])
    
    # Protein -observed_in- PMID
    for pmid, proteins_to_counts in pmid_to_protein_to_count.items():
        for protein, count in proteins_to_counts.items():
            edge_writer.writerow(['Protein:'+protein, '-observed_in->', 'PMID:'+pmid, str(1-(0.3/int(count)))])

    # PMID -studies- MeSH
    for cat, pmids in cat_to_pmids.items():
        for pmid in pmids:
            if pmid in pmid_to_protein_to_count:
                edge_writer.writerow(['PMID:'+pmid, '-studies-', 'MeSH:'+cat, '1'])
            
# Drop any duplicates
edge_df = pd.read_table(edge_path)
edge_df = edge_df.drop_duplicates()
edge_df.to_csv(edge_path, sep = '\t', index=False) 



### Nodes
with open(node_path,'w') as fout:
    node_writer = csv.writer(fout, delimiter = '\t')
    node_writer.writerow(['node', 'node_type'])
    
    # MeSH Nodes
    node_writer.writerow([f'MeSH:{graph_name}_Root', f'{graph_name}_MeSH'])
    for cat in cat_to_pmids:
        node_writer.writerow(['MeSH:'+cat, f'{graph_name}_MeSH'])
    
    # PMID Node 
    for pmids in cat_to_pmids.values():
        for pmid in pmids:
            if pmid in pmid_to_protein_to_count:
                node_writer.writerow(['PMID:'+pmid, 'PMID'])
 
    # Protein Node
    for protein in all_proteins:
        node_writer.writerow(['Protein:'+protein, 'Protein'])

# Remove any duplicates
node_df = pd.read_table(node_path)
node_df = node_df.drop_duplicates()
node_df.to_csv(node_path, sep = '\t', index=False)
