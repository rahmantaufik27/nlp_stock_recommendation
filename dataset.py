import sys
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# GET DATA FROM DATABASE 
def data_ticker_news():
    ticker_list = ("AAPL.O", "PFE", "JPM")
    engine = create_engine(os.getenv("DBURL"))
    query = f"SELECT nt.ticker, n.news FROM news_ticker as nt INNER JOIN news as n ON nt.story_id=n.story_id WHERE nt.ticker IN {ticker_list}"
    with engine.connect() as conn:
        ResultProxy = conn.execute(query)
        ResultSet = ResultProxy.fetchall()
    engine.dispose()
    df = pd.DataFrame(ResultSet)
    df.columns = ["ticker", "news"]
    return df

# GET NEWS AND RETURN AS A LIST OF DOCUMENT
def data_news():
    raw_data = data_ticker_news() 
    news = raw_data['news']
    docs = []
    for n in news:
        docs.append(n)
    return docs
