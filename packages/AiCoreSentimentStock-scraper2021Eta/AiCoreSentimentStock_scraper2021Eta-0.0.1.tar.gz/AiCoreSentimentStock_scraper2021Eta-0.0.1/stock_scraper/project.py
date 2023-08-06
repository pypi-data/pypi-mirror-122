# from stock_scraper import StockScraper
from process import stockData,stockHeadlineData,sentimentData
from data_base import SqlDB
import pandas as pd
from Sentiment_analysis import sentimentAnalysis
from process import *

# Declaring datatable names
dt_stockContent = "stock_content"
dt_headlines = "stock_headlines"
dt_sentiment = "stock_sentiment"

stockData(stockContent_name=dt_stockContent, updateFlag=True)
stockHeadlineData(headlineDatatable_name = dt_headlines, stockInfoDatatable_name = dt_stockContent, updateFlag = True)
sentimentData(sentimentDatatable_name=dt_sentiment, updateFlag=True, headlineDatatable_name=dt_headlines)


