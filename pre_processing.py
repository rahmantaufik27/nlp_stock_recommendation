import sys
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path
# from autocorrect import spell
# nltk.download('wordnet')
# nltk.download('words')
# nltk.download('punkt')
# nltk.download('stopwords')

# CLEANING
def clean_text(texts):
    # text lower case
    text_clean = texts.lower()
    # get only alphabet text
    text_clean = re.sub("[^A-Za-z]+", " ", text_clean)
    
    return text_clean

# TOKENIZING
def tokenize_text(texts):
    all_sentences = nltk.sent_tokenize(texts)
    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    return all_words

# STOPWORD PROCESS
def stopwords_fin():
    data_file = Path('stopwords/stopwords_genericlong.txt')
    f = open(data_file)
    stopwords = f.read()
    return stopwords

def stopwords_key():
    data_file = Path('stopwords/stopwords_keywords.txt')
    f = open(data_file)
    stopwords = f.read()
    return stopwords

def remove_wordstop(words):
    # remove words listed on stopwords
    stop = stopwords_key()
    stop = stop.splitlines()
    stop = str(stop)
    stop = stop.translate(str.maketrans('', '', string.punctuation))
    
    stopwords_list = list(stopwords.words('english'))
    stopwords_list.extend(stop.split())

    for i in range(len(words)):
        words[i] = [w for w in words[i] if w not in stopwords_list]
    return words    

# LEMMATIZATION
def lemmatization_text(words):
    lemmatizer = WordNetLemmatizer()
    lemma_text = []
    for word in words:
        lemma_text.append(lemmatizer.lemmatize(word))
    return lemma_text

# STEMING
def stemming_text(words):
    englishStemmer = SnowballStemmer("english")
    stem_text = []
    for word in words:
        stem_text.append(englishStemmer.stem(word))
    return stem_text

def pre_process(docs):
    text_processed = str(docs)
    text_processed = clean_text(text_processed)
    text_processed = tokenize_text(text_processed)
    text_processed = remove_wordstop(text_processed)
    return text_processed
