import sys
import nltk
import string
import pandas as pd
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import datapath
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from pre_processing import pre_process
from dataset import data_news_keywords, data_news_rank

# RETURN KEYWORD AND VECTORS FROM QUESTION
def test_data(text, model_name):
    print("===SEARCH===")
    print(text)
    
    print("===KEYWORDS===")
    words = pre_process(text)
    print("{}".format(words[0]))

    model_name = 'data_corpus/' + model_name
    model = KeyedVectors.load_word2vec_format(model_name, binary=True)
    data_sim_words = []
    sim_words = []
    print("===VECTORS===")
    for q in words[0]:
        try:
            vector = model.wv[q]
            voc = True
        except Exception as e:
            vector = ''
            print("- {} not in corpus".format(q))
            voc = False
            sim_words += []

        if voc:
            # print("- nearest vectors of {}:".format(q))
            sim_words = model.wv.most_similar(q)
            # print(sim_words)
            data_sim_words += sim_words

    return data_sim_words

# RETURN TICKER RECOMMENDATION BASED ON KEYWORD
def test_ticker_recommender(keywords):
    # print(keywords)
    print("===TICKERS===")
    print('- recommendation tickers:')
    # keywords = keywords[:2]
    tickers = []
    ticker_recommend = data_news_keywords(keywords)
    if ticker_recommend != '':
        ticker_recommend = tuple(ticker_recommend)
        ticker_recommend = data_news_rank(ticker_recommend)
        print(ticker_recommend[:10])
    else:
        print("there is no ticker recommendation")
