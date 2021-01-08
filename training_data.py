import sys
import nltk
import string
import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import datapath
from gensim.models import translation_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors
from pre_processing import stopwords_key
from textblob import TextBlob

# WORD2VEC SKIP-GRAM MODEL
def w2v_skip_gram(data):
    model = Word2Vec(data, min_count=1, size=300, window=5, workers=4, sg=1)
    return model

# WORD2VEC CBOW MODEL
def w2v_bow(data):
    model = Word2Vec(data, min_count=1, size=300, window=5, workers=4)
    return model

# EXECUTE WORDS EMBEDDING MODEL
def create_model(data, model_name):
    model = w2v_skip_gram(data)
    # model_name1 = 'data_corpus/' + model_name + '.model'
    model_name2 = 'data_corpus/' + model_name + '.bin'
    model_name3 = 'data_corpus/' + model_name + '.txt'

    # data_model = model.save(model_name1)
    model.wv.save_word2vec_format(model_name2, binary=True)
    model.wv.save_word2vec_format(model_name3, binary=False)

# TRAINING DATA TO GET WORDS EMBEDDEDS
# words embedding use word2vec model
# the result is corpus model containing dimensional word vectors
def train_data(data, model_name):
    data_model_processed = data
    create_model(data_model_processed, model_name)
    print("training data is done")

# TRAINING DATA TO GET KEYWORDS
# training news per each tickers using TF-IDF2
# the result is list of important keywords and vectors for each ticker
def train_keyword(data):
    stop = stopwords_key()
    stop = stop.splitlines()
    stop = str(stop)
    stop = stop.translate(str.maketrans('', '', string.punctuation))
    
    stopwords_list = list(stopwords.words('english'))
    stopwords_list.extend(stop.split())
    vectorizer = TfidfVectorizer(analyzer='word', stop_words=set(stopwords_list), use_idf=True)
    vector = vectorizer.fit_transform(data)
    df = pd.DataFrame(vector[0].T.todense(), index=vectorizer.get_feature_names(), columns=["vector"])
    df = df.sort_values('vector', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'keywords'})
    df = df[df['vector'] != 0]

    return df.head(10)

# TRAINING DATA TO GET RANKING
# training ranking use sentiment analysis (textblob tool)
def training_sentiment(news):
    df = pd.DataFrame(news, columns=['news'])
    df['polarity'] = np.nan
    df['subjectivity'] = np.nan
    df['score'] = np.nan

    for idx, n in enumerate(df['news']):
        sent_analysis = TextBlob(n)
        df['polarity'].iloc[idx] = sent_analysis.sentiment.polarity
        df['subjectivity'].iloc[idx] = sent_analysis.sentiment.subjectivity
        if sent_analysis.sentiment.polarity >= 0.05:
            score1 = 'positive'
        elif -0.05 < sent_analysis.sentiment.polarity < 0.05:
            score1 = 'neutral'
        else:
            score1 = 'negative'
        df['score'].iloc[idx] = score1   
    return df

# IF THE CORPUS WANT TO EXPANDED BY ANOTHER PRETRAINED
def expanded_pretrained():
    # list of pretrained
    filenames = ['data_corpus/GoogleNews-vectors-negative300.bin', 'data_corpus/model_wiki_en.bin', 'data_corpus/asklora_mega_corpus.bin', 'data_corpus/glove-wiki-gigaword-300.bin']
    out_data = b''

    # merge into one corpus model
    for fn in filenames:
        with open(fn, 'rb') as fp:
            out_data += fp.read()
    with open('data_corpus/pretrained_all.bin', 'wb') as fp:
        fp.write(out_data)

# IF THE MODEL WANT TO BE REFORMATED
def model_reformated(filename):
    wv = KeyedVectors.load_word2vec_format(f"data_corpus/{filename}.bin", binary=True)
    wv.save_word2vec_format(f"data_corpus/{filename}.txt", binary=False)