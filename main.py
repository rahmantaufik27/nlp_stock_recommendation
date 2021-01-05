import sys
import argparse
import os
import datetime
import pandas as pd
from tqdm import tqdm
from testing_data import test_testing
from training_data import train_data
from pre_processing import pre_process
from dataset import data_ticker_news, data_news

parser = argparse.ArgumentParser()
parser.add_argument('--train_model', action='store_true', help='training model using current data and generate into one large corpus model')
parser.add_argument('--test_model', action='store_true', help='testing model using current data')
args = parser.parse_args()

if __name__ == '__main__':

    # TRAINING DATA INTO A CORPUS MODEL
    if args.train_model:
        # import data first
        raw_data = data_news()
        pbar = tqdm(raw_data)
        doc_old = raw_data
        doc_new = []
        
        # pre-processing the data (including cleaning, tokenizing, remove stopwords, etc.)
        for doc in doc_old:
            pbar.set_description("requesting for : %s" % doc)
            doc_new += pre_process(doc)


        # training data
        train_data(doc_new, 'news_corpus')
    elif args.test_model:
        test_testing()