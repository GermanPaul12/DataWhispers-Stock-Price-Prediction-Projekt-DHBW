# Importing necessary libraries
# numpy for numerical operations
# gensim for word embeddings and NLP
# sklearn for machine learning tasks
# nltk for natural language processing
# pandas for data manipulation
# gensim.downloader to download pretrained models
# preprocessing script for text processing
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import gensim.downloader as api
from preprocess import preprocess_text
from gensim.models.keyedvectors import Word2VecKeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from sklearn.metrics.pairwise import cosine_similarity
## defining global variables
import os
import platform

os_ = platform.system()
op = "/"
print(os_)
if os_ == "Windows":
    op = "\\"
    
datapath = f"{op}".join(["models", "word2vec-google-news-300.model"])
datapath_vec = f"{op}".join(["models", "word2vec-google-news-300.model.vectors.npy"])
models_path = f"models{op}"
glove_input_file = "glove.twitter.27B.200d.txt"
glove_version = glove_input_file.split('.')[3]
dimensions = int(glove_input_file.split('.')[3][:-1])

## loading pretrained models
model = KeyedVectors.load_word2vec_format(models_path + glove_input_file, binary=False, no_header=True)

## loading data
data = pd.read_csv('data/preprocessed_data.csv', index_col=0)
#data = data. head(500)
feature = 'title'

## preprocessing data
data['feature_clean'] = data[feature].apply(preprocess_text)
data = data[data[feature].notna()]


## vectorizes a list of words
def vectorize_word_list(word_list):
    vectorized_list = []
    for word in word_list:
        try:
            vectorized_list.append(model[word])
        except KeyError:
            pass
    return np.array(vectorized_list)


## vectorizes the categories
def preprocess_categories(categories):
    categories_list = []
    for category in categories:
        splited_categories = category.split(" ")
        categories_list.append(splited_categories)
    return categories_list


## vectorizing features
data['feature_vectorized_mean'] = data['feature_clean'].apply(vectorize_word_list).apply(lambda x: np.mean(x, axis=0))
assert data.iloc[0]['feature_vectorized_mean'].shape == (dimensions,)


## defining and preprocessing categories
categories = ["political instability", "geopolitical factors", "currency fluctuations", "investment demand", "supply demand", 
"industrial demand", "natural disasters"]
pc = preprocess_categories(categories)
vectorized_categories = np.mean(vectorize_word_list(pc), axis=1)
assert vectorized_categories.shape == (7, dimensions)


## compute similarity between an entry and categories
def compute_similarity_with_categories(feature_vectorized_mean):
    similarity_list = []
    for category in vectorized_categories:
        #print(cosine_similarity(feature_vectorized_mean.reshape(1, -1), category.reshape(1, -1)))
        similarity_list.append(cosine_similarity(feature_vectorized_mean.reshape(1, -1), category.reshape(1, -1))[0])
    return similarity_list


# compute similarity between the entries and the categories
data_regression = data['feature_vectorized_mean'].apply(compute_similarity_with_categories)

## saving output to file
data_regression_convert = pd.DataFrame(np.array(data_regression.to_list()).reshape(-1, 7), columns=categories)
data_regression_convert['date'] = data['date'].values

data_regression_convert.to_csv(f"./regression_data/data_regression_{feature}_{glove_version}.csv")
data_regression_convert.to_pickle(f"./regression_data/data_regression_{feature}_{glove_version}.pickle")

# print output shape
print(data_regression.shape)