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
# from pre_processing import pre_process

def test_testing():
    print('testing')
    sys.exit()


def get_similarities(text):
    try: 
        sim_words = model.wv.most_similar(question[0])
        res = sim_words
    except Exception as e:
        res = ''
    return res


def test_data(text, model_name, i):
    print("===SEARCH===")
    print(text[i])
    words = []
    for t in text:
        words += pre_process(str(t))
    
    print("===KEYWORDS===")
    question = words[i]
    print("{}".format(question))

    model_name = 'data_corpus/' + model_name
    model = KeyedVectors.load_word2vec_format(model_name, binary=True)
    data_sim_words = []
    sim_words = []
    print("===VECTORS===")
    for q in question:
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
    
# class SearchToTicker(viewsets.ModelViewset):

def test_comparison_data(keywords):
    # print(keywords)
    print("===TICKERS===")
    print('- recommendation tickers:')
    # keywords = keywords[:2]
    tickers = []
    # queryset = NewsTickerKeyword.objects.filter(keyword__in=keywords).order_by('-ticker__ticker_news_rating__number_positive')
    queryset = NewsTickerKeyword.objects.filter(keyword__in=keywords).distinct('ticker').values('ticker')
    # queryset = queryset[:10]
    # print(queryset)
    for qs in queryset:
        # print(qs)
        tickers.append(qs['ticker'])
    # print(tickers)
    queryset2 = DroidUniverseNewsRating.objects.filter(ticker__in=tickers).order_by('-number_positive')
    queryset2 = queryset2[:10]
    for qs2 in queryset2:
        print(qs2)


