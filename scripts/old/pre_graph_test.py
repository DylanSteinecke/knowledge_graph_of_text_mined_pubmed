import json
import csv
import pandas as pd

pmid_to_protein_to_count = json.load(open('../data/metadata_pmid2pcount.json'))

pmids_in_cats = json.load(open('../data/textcube_category2pmid.json'))
cat_names = json.load(open('../data/textcube_config.json'))

'''Map Category name to PMIDs'''
cat_to_pmids = dict()
for num, pmid_list in enumerate(pmids_in_cats):
    cat_name = cat_names[num]
    cat_to_pmids[cat_name] = pmid_list
    
    
'''Collect all proteins'''
all_proteins = set()
for proteins_to_counts in pmid_to_protein_to_count.values():
    for protein in proteins_to_counts:
        all_proteins.add(protein)
all_proteins = list(all_proteins)



'''Write in graph-ready csv format'''
node_path = '../data/node_list.tsv'
edge_path = '../data/edge_list.tsv'
test_pmids = list()

### Nodes
with open(node_path,'w') as fout:
    writer = csv.writer(fout, delimiter = '\t')
    writer.writerow(['node', 'node_type'])
    
    # OS MeSH Node
    writer.writerow(['MeSH:OS_Root', 'OS_MeSH'])
    for cat in cat_to_pmids:
        writer.writerow(['MeSH:'+cat, 'OS_MeSH'])
    
    # PMID Node 
    for pmids in cat_to_pmids.values():
        for pmid in pmids:
            writer.writerow(['PMID:'+pmid, 'PMID'])
            test_pmids.append(pmid)
            break
 
    # Protein Node
    for protein in all_proteins:
        writer.writerow(['Protein:'+protein, 'Protein'])

# Remove any duplicates
df = pd.read_table(node_path)
df = df.drop_duplicates()
df.to_csv(node_path, sep = '\t', index=False)


### Edges
with open(edge_path,'w') as fout:
    writer = csv.writer(fout, delimiter = '\t')
    writer.writerow(['head', 'relation', 'tail', 'weight'])

    # MeSH 'Tree'
    for cat in cat_to_pmids:
        writer.writerow(['MeSH:OS_Root', '-parent_of->', 'MeSH:'+cat, '1'])
    
    # PMID -studies- MeSH
    for cat, pmids in cat_to_pmids.items():
        for pmid in pmids:
            if pmid in test_pmids:
               writer.writerow(['PMID:'+pmid, '-studies-', 'MeSH:'+cat, '1'])
            
    # Protein -observed_in- PMID
    for pmid, proteins_to_counts in pmid_to_protein_to_count.items():
        for protein, count in proteins_to_counts.items():
           if pmid in test_pmids:
              writer.writerow(['Protein:'+protein, '-observed_in->', 'PMID:'+pmid, str(1-(0.3/int(count)))])
            
# Drop any duplicates
df = pd.read_table(edge_path)
df = df.drop_duplicates()
df.to_csv(edge_path, sep = '\t', index=False)
