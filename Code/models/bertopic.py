# Importing necessary libraries
# BERTopic for topic modeling
# pandas for data manipulation
# nltk for natural language processing
# numpy for numerical operations
from bertopic import BERTopic
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np

# Initializing the BERTopic model with probability calculation enabled
model = BERTopic(calculate_probabilities=True)
# Loading the preprocessed data from a CSV file into a pandas DataFrame
# Resetting the index of the DataFrame
df = pd.read_csv("preprocessed_data.csv", index_col=0).reset_index()

# Downloading necessary NLTK resources
# 'stopwords' for stop words removal
# 'punkt' for tokenization
nltk.download('stopwords')
nltk.download('punkt')
# Creating a set of English stop words for text processing
stoplist = set(stopwords.words("english"))

# Defining a function to remove stop words from a document
# The function takes a string as input and returns a list of words
def remove_stopwords(document):
    word_lst =[]
    # split the text by whitespace
    for word in document.split():
        if word.lower() not in stoplist:
            word_lst.append(word)
    # return the document as a string
    return ' '.join(word_lst)

no_stopwords_df = df.copy()
no_stopwords_df["content"] = no_stopwords_df["content"].apply(remove_stopwords)

# %%
category_lst = ["political instability",
                "geopolitical factors",
                "currency fluctuations",
                "investment demand",
                "supply and demand",
                "industrial demand",
                "natural disasters"]

# function which creates an array for a word based on the similarities scores returned by the find_topics method
def create_category_vector(category, num_topics):
    topics = model.find_topics(category, top_n=num_topics)
    topic_lst = topics[0]
    prob_lst = topics[1]
    array = np.zeros(num_topics)
    for lst_idx, topic_idx in enumerate(topic_lst):
        # ignore -1 which means outlier (topic)
        if topic_idx != -1:
            array[topic_idx] = prob_lst[lst_idx]
    return array

# function to iterate over all documents probabilities
def create_doc_embeddings(similarities):
    """
    # create an embedding for every document in every category, e.g. political stability and return 7 dimensional array

    # every document has a similarity score for every topic created by BERTopic
    # compute the cosine similarity of the similarity score vector of the document and the category
    """
    num_categories = len(category_lst)
    embedding_lst = []
    for doc in similarities:
        array = np.zeros(num_categories)
        for array_idx, category_embedding in enumerate(category_embeddings):
            doc_embedding = np.array(doc)
            dot_product = np.dot(category_embedding, doc_embedding)
            norm_doc = np.linalg.norm(doc_embedding)
            norm_category = np.linalg.norm(category_embedding)
            cosine_similarity = dot_product / (norm_doc * norm_category)
            array[array_idx] = cosine_similarity
        embedding_lst.append(array)
    return embedding_lst


# %%
topics, similarities = model.fit_transform(no_stopwords_df["content"])

# creating an embedding for each element in the category_lst
num_topics = len(np.unique(topics)) - 1
category_embeddings = [create_category_vector(category, num_topics) for category in category_lst]

# creating embedding and saving as a df
embedding_lst = create_doc_embeddings(similarities)
embedding_df = pd.DataFrame(embedding_lst)
embedding_df.columns = category_lst
embedding_df['date'] = df['date']

# %%
from umap import UMAP
from bertopic.dimensionality import BaseDimensionalityReduction
from sklearn.cluster import KMeans
from hdbscan import HDBSCAN

# hyperparameters
embedding_model_lst = ["all-MiniLM-L12-v2", "all-mpnet-base-v2", "all-distilroberta-v1"]

umap = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
empty_dimensionality_model = BaseDimensionalityReduction()
umap_model_lst = [umap, empty_dimensionality_model]
umap_model_names = ["umap", "empty"]

# grid search
for embedding_model in embedding_model_lst:
    for umap_model, umap_model_name in zip(umap_model_lst, umap_model_names):
        model = BERTopic(embedding_model=embedding_model,
                          umap_model=umap_model,
                          calculate_probabilities=True)
        topics, similarities = model.fit_transform(no_stopwords_df["content"])

        num_topics = len(np.unique(topics)) - 1
        category_embeddings = [create_category_vector(category, num_topics) for category in category_lst]

        embedding_lst = create_doc_embeddings(similarities)

        # embeddings without normalization
        embedding_df = pd.DataFrame(embedding_lst)
        embedding_df.columns = category_lst
        embedding_df['date'] = df['date']
        embedding_df.to_csv(f"{embedding_model}_{umap_model_name}.csv")

        # embeddings with normalization
        norm_embedding_df = embedding_df.copy()
        norm_embedding_df.iloc[:,0:-1] = norm_embedding_df.iloc[:,0:-1].apply(lambda x: (x-x.mean())/ x.std(), axis=0)
        norm_embedding_df.to_csv(f"{embedding_model}_{umap_model_name}_normalized.csv")

