import sys
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# GET TICKER FROM DATABASE
def data_ticker():
    try:
        engine = create_engine(os.getenv("DBURL"))
        query = "SELECT ticker FROM droid_universe WHERE is_active = True"
        with engine.connect() as conn:
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
        engine.dispose()
        df = pd.DataFrame(ResultSet)
        df.columns = ["ticker"]
        ticker = df['ticker']
        tickers = []
        for t in ticker:
            tickers.append(t)
    except Exception as e:
        print(e)
    return tickers

# GET TICKER DESCRIPTION FROM DATABASE
def data_ticker_des(ticker_list):
    # ticker_list = ("AAPL.O", "PFE", "JPM")
    try:
        engine = create_engine(os.getenv("DBURL"))
        query = f"SELECT long_des FROM company_descriptions WHERE ticker IN {ticker_list}"
        with engine.connect() as conn:
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
        engine.dispose()
        df = pd.DataFrame(ResultSet)
        df.columns = ["long_des"]
        des = df["long_des"]
        docs = []
        for d in des:
            docs.append(d)
        return docs
    except Exception as e:
        print(e)
    return df

# GET NEWS PER TICKER FROM DATABASE 
def data_ticker_news(ticker_list):
    # ticker_list = ("AAPL.O", "PFE", "JPM")
    try:
        engine = create_engine(os.getenv("DBURL"))
        query = f"SELECT n.news FROM news_ticker as nt INNER JOIN news as n ON nt.story_id=n.story_id WHERE nt.ticker IN {ticker_list}"
        with engine.connect() as conn:
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
        engine.dispose()
        df = pd.DataFrame(ResultSet)
        df.columns = ["news"]
        news = df["news"]
        docs = []
        for n in news:
            docs.append(n)
        return docs
    except Exception as e:
        print(e)
    return docs

# GET NEWS AND RETURN AS A LIST OF DOCUMENT
def data_news():
    raw_data = data_ticker_news() 
    news = raw_data['news']
    docs = []
    for n in news:
        docs.append(n)
    return docs

def data_news_keywords(keywords):
    keywords = tuple(keywords)
    try:
        engine = create_engine(os.getenv("DBURL"))
        query = f"SELECT ticker FROM news_ticker_keywords WHERE keyword IN {keywords}"
        with engine.connect() as conn:
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
        engine.dispose()
        df = pd.DataFrame(ResultSet)
        df.columns = ["ticker"]
        ticker = df['ticker']
        tickers = []
        for t in ticker:
            tickers.append(t)
    except:
        tickers = ''
    return tickers

def data_news_rank(ticker_list):
    try:
        engine = create_engine(os.getenv("DBURL"))
        query = f"SELECT n.ticker, du.ticker_name FROM news_ticker_rating as n INNER JOIN droid_universe as du ON n.ticker=du.ticker WHERE n.ticker IN {ticker_list} ORDER BY number_positive DESC"
        with engine.connect() as conn:
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
        engine.dispose()
        df = pd.DataFrame(ResultSet)
        df.columns = ["ticker", "company"]
    except:
        df = ''
    return df
