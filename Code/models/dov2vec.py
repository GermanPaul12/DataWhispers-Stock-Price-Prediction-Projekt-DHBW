# Importing necessary libraries
# docarray for document array operations
# pandas for data manipulation
# sklearn for machine learning utilities
# numpy for numerical operations
from docarray import BaseDoc
from docarray.typing import NdArray
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Loading preprocessed data from a CSV file into a pandas DataFrame
# The first column is used as the index column
data = pd.read_csv('data/preprocessed_data.csv', index_col=0)
# Setting the vector dimension size for the Doc2Vec model and the number of training epochs
vector_dimension = 256
epochs = 50
#data = data.head(200)

# Importing Doc2Vec and TaggedDocument from gensim for document embedding
# Importing word_tokenize from nltk for tokenization of text
from gensim.models.doc2vec import Doc2Vec,\
	TaggedDocument
from nltk.tokenize import word_tokenize

# Preprocessing the documents to create TaggedDocuments
# TaggedDocuments are used for training the Doc2Vec model
tagged_data = [TaggedDocument(words=word_tokenize(doc.lower()),
							tags=[str(i)]) for i,
			doc in enumerate(data['content'])]

# train the Doc2vec model
model = Doc2Vec(vector_size=vector_dimension,
				min_count=2, epochs=epochs)
model.build_vocab(tagged_data)
model.train(tagged_data,
			total_examples=model.corpus_count,
			epochs=model.epochs)

# # get the document vectors
# document_vectors = [model.infer_vector(
# 	word_tokenize(doc.lower())) for doc in data]

# # print the document vectors
# for i, doc in enumerate(data):
# 	print("Document", i+1, ":", doc)
# 	print("Vector:", document_vectors[i])
# 	print()


categories = ["political instability", "geopolitical factors", "currency fluctuations", "investment demand", "supply demand", 
"industrial demand", "natural disasters"]

categories_enc = [model.infer_vector(word_tokenize(category.lower())) for category in categories]

#model.infer_vector(word_tokenize('natural disaster'.lower()))


def calculate_scores(entry, type='content'):
    sentence_embeddings = model.infer_vector(word_tokenize(entry[type].lower()))
    sentence_embeddings = categories_enc + [sentence_embeddings]
    scores = []
    for i in range(len(categories)):
        scores.append(cosine_similarity(sentence_embeddings[i].reshape(1, -1), sentence_embeddings[-1].reshape(1, -1)))
    return np.array(scores)


data_regression = data.apply(calculate_scores, axis=1)

feature = 'content'
data_regression_convert = pd.DataFrame(np.array(data_regression.to_list()).reshape(-1, 7), columns=categories)
data_regression_convert['date'] = data['date'].values

data_regression_convert.to_csv(f"./regression_data/data_regression_doc2vec_{feature}_{vector_dimension}_e{epochs}.csv")
data_regression_convert.to_pickle(f"./regression_data/data_regression_doc2vec_{feature}_{vector_dimension}_e{epochs}.pickle")