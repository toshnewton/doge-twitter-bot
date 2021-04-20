import os
import logging
from time import sleep
import tweepy
from requests import Request, Session
import json
from config import *
from credentials import COIN_API_KEY

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

def initialize_api():
    api = create_api()
    return api


def get_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {'symbol': 'DOGE'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COIN_API_KEY}
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    logger.info("Collected Doge Data")

    return float(data['data']['DOGE']['quote']['USD']['price'])

def createDogeStatus(dogePrice):
    if (dogePrice < 1.0):
        status = "No, the price is {}".format(dogePrice)
        logger.info("Created Status")
    else:
        status = "Yes, the price is {}".format(dogePrice)
        logger.info("Created Status")
    return status

def writeTweet(status):   
    try:
        api.update_status(status)
        logger.info("Uploaded Status")
    except Exception as e:
        logger.error("Error on status update", exc_info=True)
        raise e

if __name__ == "__main__":
    api = initialize_api()
    dogePrice = get_price()
    status = createDogeStatus(dogePrice)
    writeTweet(status)
