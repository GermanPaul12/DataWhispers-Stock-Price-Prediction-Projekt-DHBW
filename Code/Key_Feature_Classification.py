#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:22:40 2023

@author: jw124
"""

# libraries
import pandas as pd
import numpy as np
import regex as re
import string
from collections import deque
from typing import List, Union, Dict, Set, Tuple, Sequence

# nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader.wordnet import Synset
from nltk import pos_tag
# from nltk.stem import PorterStemmer


# load data
df_prepro_data = pd.read_csv('/home/jw124/dhbw/3_semester/methoden_wirtschaftsinformatik/DataWhispers-Stock-Price-Prediction-Projekt-DHBW/Inspiration/abgabe-MSGladiators/data/preprocessed_data.csv')
df_prepro_data = df_prepro_data[df_prepro_data['title'].notna()]

# function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Stemming
    # stemmer = PorterStemmer()

    # Removing stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Normalization (converting to lower case and removing punctuation)
    normalized_tokens = [re.sub(r'[^\w\s]', '', word.lower()) for word in filtered_tokens]
    normalized_tokens = [word for word in normalized_tokens if word]  # Remove empty strings
    normalized_tokens = [word for word in normalized_tokens if not word.isdigit()] # Remove numbers
    normalized_tokens = [word for word in normalized_tokens if not len(word) == 1] # Remove single characters
    normalized_tokens = [word for word in normalized_tokens if pos_tag([word])[0][1] in ['NN', 'NNS', 'NNP', 'NNPS']] # Remove non-nouns
    normalized_tokens = [word for word in normalized_tokens if word not in string.punctuation] # Remove punctuation
    normalized_tokens = list(filter(lambda x: not re.search(r'\d', x), normalized_tokens)) # Remove tokens with numbers
    # normalized_tokens = list({stemmer.stem(token) for token in normalized_tokens}) # Stemming

    return normalized_tokens


# Build-up functions that calculate the similarity between two words 

def shortest_paths_to(start_syn: Synset) -> Dict[Synset, int]:
    """Compute the shortest distance to all nodes on paths to the root.
    :param start_syn: synset to which we want to compute the shortest distances
    :return: dict that matches all visited hypernyms to their distance to the input synset  
    """ 
    # create set that keeps track of visited nodes
    visited = set()
    # create list which stores nodes (including distances) that need to be processed
    queue = [(start_syn, 0)]
    # create result dicitionary
    distances = {}

    # check nodes in the list queue as long it is not empty
    while len(queue) > 0:
        # remove nodes from front of list
        syn, dist = queue.pop(0)
        # check unvisited synsets
        if syn in visited:
            continue
        visited.add(syn)
        distances[syn] = dist
        # loop over all direct hypernyms in list (input synset might be an instance)
        for hyp in syn.hypernyms() + syn.instance_hypernyms():
            # append it to queue (with dist+1) if not already looked at it before
            if hyp not in visited or distances[hyp] > dist + syn.path_similarity(hyp):
                queue.append((hyp, dist + syn.path_similarity(hyp)))
                distances[hyp] = dist + syn.path_similarity(hyp)
            # we only want to store the shortest distances
            elif distances[hyp] > dist + syn.path_similarity(hyp):
                distances[hyp] = dist + syn.path_similarity(hyp)
    return distances

def merge_paths(p1: Dict[Synset, int], p2: Dict[Synset, int]) -> Dict[Synset, int]:
    """Merge two paths keeping the shorter distance for synsets that appear more than once.
    :param p1: first dict that maps synsets to their shortest distances
    :param p2: second dict that maps synsets to their shortest distances
    :return: merged dict
    """
    # create resulting dictionary
    merged = {}
    # loop over all keys of both dictionaries
    for synset in set(p1.keys()) | set(p2.keys()):
        # for synsets in p1 and p2 we keep the shorter distance
        if synset in p1 and synset in p2:
            merged[synset] = min(p1[synset], p2[synset])
        # distance of p1 if synset only appears in p1
        elif synset in p1:
            merged[synset] = p1[synset]
        # distance of p2 if synset only appears in p2
        else:
            merged[synset] = p2[synset]
            
    return merged

def all_hypernym_paths(word: str) -> Dict[Synset, int]:
    """Get all hypernyms of all synsets associated with the input word and compute the shortest distance leading there.
    :param word: input word
    :return: dict that matches all reachable hypernyms to their shortest distance 
    """
    # get synsets of input word
    synsets = wn.synsets(word)
    # create resulting dictionary
    distances = {}

    # using our functions of tasks a) and b)
    for synset in synsets:
        paths = shortest_paths_to(synset)
        distances = merge_paths(distances, paths)

    return distances

def get_dist(w1 : str, w2 : str) -> float:
    """Compute the similarity between two input words in the WordNet hierarchy tree.
    :param w1: first input word
    :param w2: second input word
    :return: word similarity
    """
    # use function from c)
    hyp1 = all_hypernym_paths(w1)
    hyp2 = all_hypernym_paths(w2)
    # filter on hypernyms that occur in both hypernym dictionaries
    hyps = {k : hyp1[k] for k in hyp1 if k in hyp2}
    # define d as shortest distance
    if len(hyps) > 0:
        d = min(hyps.values())
        return d
    else:
        return 0
    
# list of key features
key_features = ['politics instability' , 'geopolitics factor' , 'currency fluctuation' ,
                'investment demand' , 'supply and demand' , 'industry demand' , 'nature disaster']
key_features_original = ['political instability' , 'geopolitical factors' , 'currency fluctuations' ,
                        'investment demand' , 'supply and demand' , 'industrial demand' , 'natural disasters']
key_features_weights = [[2/5, 3/5],[4/5, 1/5], [1/2, 1/2], [4/5, 1/5], [4/5, 1/5], [4/5, 1/5], [2/5, 3/5]]

key_features_normalized = [preprocess_text(key) for key in key_features]

# final classifier function
def text_classifier(titles: List[str], key_features_tokens: List[List[str]]) -> pd.DataFrame:
    # Initialize a DataFrame to store the classification results
    df_classifier = np.zeros((len(titles), len(key_features_tokens)))

    # Precompute distances between title tokens and key feature tokens
    # This will be a dictionary where the key is a tuple (title_token, key_feature_token)
    # and the value is the computed distance.
    precomputed_distances = {}

    for i, title in enumerate(titles):
        title_tokens = preprocess_text(title)
        if not title_tokens:
            continue
        print(i)
        for idx_kf, key_feature in enumerate(key_features_tokens):
            distances = []
            print(key_feature)
            for title_token in title_tokens:
                for j, key_feature_token in enumerate(key_feature):
                    print(title_token)
                    # Check if the distance is already computed
                    if (title_token, key_feature_token) not in precomputed_distances:
                        distance = get_dist(title_token, key_feature_token)
                        precomputed_distances[(title_token, key_feature_token)] = distance
                    else:
                        distance = precomputed_distances[(title_token, key_feature_token)]

                    distances.append(distance * key_features_weights[idx_kf][j])

            # Calculate average distance for the current title and key feature
            if distances:
                avg_distance = sum(distances) / len(distances)
                df_classifier[i, idx_kf] = avg_distance

    return pd.DataFrame(df_classifier, columns=key_features_original)


# create dataset with classifications
classifications = text_classifier(df_prepro_data['title'], key_features_normalized)
classifications['date'] = df_prepro_data['date']
classifications.to_csv('./data/classification_wordnet.csv', index=False)
    
