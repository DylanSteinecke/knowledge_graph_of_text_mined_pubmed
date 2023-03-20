import os
import json
from transformers import AutoTokenizer, AutoModel


node_to_text_inf = os.path.join('..', 'data', 'os_node_to_text.json')

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')

# Text to embed
node_to_text = json.load(open(node_to_text_inf))
text = list(node_to_text.values())[:10]

# preprocess the input
inputs = tokenizer(text, 
                   padding = True, 
                   truncation = True, 
                   return_tensors = 'pt', 
                   max_length = 1024)
result = model(**inputs)

# take the first token in the batch as the embedding
node_features = result.last_hidden_state[:, 0, :]


node_names = list(node_to_text.keys())
node_df = pd.DataFrame(node_features, index = node_names[:len(node_features)])