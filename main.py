import sys
import argparse
import os
import datetime
import pandas as pd
from tqdm import tqdm
from testing_data import test_data, test_ticker_recommender
from training_data import train_data, model_reformated, training_sentiment, train_keyword
from pre_processing import pre_process
from dataset import data_ticker_news, data_ticker, data_ticker_des

parser = argparse.ArgumentParser()
parser.add_argument('--train_model', action='store_true', help='training model using current data and generate into one large corpus model')
parser.add_argument('--train_ranking', action='store_true', help='training model into news ranking')
parser.add_argument('--train_embedding', action='store_true', help='training model into words embedding')
parser.add_argument('--train_keyword', action='store_true', help='training model into keywords')
parser.add_argument('--test_model', action='store_true', help='testing model using current data')
args = parser.parse_args()

if __name__ == '__main__':

    # TRAINING DATA INTO A CORPUS MODEL
    if args.train_model:
        # import data first
        ticker_list = data_ticker()
        ticker_list = tuple(ticker_list)
        raw_data = []
        raw_data += data_ticker_news(ticker_list)
        # raw_data += data_ticker_des(ticker_list)

        if args.train_ranking:
            # training sentiment for news ranking
            sentiment_res = training_sentiment(raw_data)
            print(sentiment_res.head())

        elif args.train_embedding:
            pbar = tqdm(raw_data)
            doc_old = raw_data
            doc_new = []

            # pre-processing the data (including cleaning, tokenizing, remove stopwords, etc.)
            for i, doc  in tqdm(enumerate(doc_old[:15000])):
                # pbar.set_description("requesting for : %s" % i)
                doc_new += pre_process(doc)

            # training words embedding
            train_data(doc_new, 'news_corpus')

        elif args.train_keyword:
            keywords = train_keyword(raw_data)
            print(keywords)

        else:
            # converted model to txt
            model_reformated('news_corpus')

    # TESTING DATA USING CORPUS MODEL
    elif args.test_model:
        # question examples
        question = [
            "information technology company?",
            "company related to covid?",
            "financial stock",
        ]

        # get words embedding from one of question
        search_this = test_data(question[1], 'asklora_mega_corpus.bin')
        print(search_this)
        keys = []

        # get keywords from the question
        for i, s in enumerate(search_this):
            # get first data in list during the loop (keyword)
            keys.append(search_this[i][0].lower())

        # get ticker recommendation based on news ranking
        test_ticker_recommender(keys)
