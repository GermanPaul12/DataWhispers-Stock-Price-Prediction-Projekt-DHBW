from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity


## read data
#import os
#print(os.getcwd())
data = pd.read_csv('data/preprocessed_data.csv', index_col=0)
#data = data.head(200)


## define categories
categories = ["political instability", "geopolitical factors", "currency fluctuations", "investment demand", "supply demand", 
"industrial demand", "natural disasters"]


## calculate categories embeddings
categories_enc = model.encode(categories)

## calculate cosine similarity of one sentence with each category
def calculate_scores(entry, type='content'):
    input = entry[type]
    sentence_embeddings = model.encode(input)
    sentence_embeddings = categories_enc + [sentence_embeddings]
    scores = []
    for i in range(len(categories)):
        scores.append(cosine_similarity(sentence_embeddings[i].reshape(1, -1), sentence_embeddings[-1].reshape(1, -1)))
    return np.array(scores)



## calculate scores for each sentence
data_regression = data.apply(calculate_scores, axis=1, type='title')
feature = 'title'


## saving scores to csv and pickle
data_regression_convert = pd.DataFrame(np.array(data_regression.to_list()).reshape(-1, 7), columns=categories)
data_regression_convert['date'] = data['date'].values

data_regression_convert.to_csv(f"./regression_data/data_regression_sentence_transformer_{feature}.csv")
data_regression_convert.to_pickle(f"./regression_data/data_regression_sentence_transformer_{feature}.pickle")

#data['tokenize'] = data['content'].apply(sent_tokenize)
#out = data.apply(lambda x: model.encode(x['tokenize']), axis=1)