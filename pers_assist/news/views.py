from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import asyncio
from datetime import datetime, timedelta
import environ
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

CURRENT_DATE = datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%d.%m.%Y")
PRIVAT_URL = f"https://api.privatbank.ua/p24api/exchange_rates?date={CURRENT_DATE_STR}"
NEWS_DAYS = 2  

NEWS_DATE = CURRENT_DATE - timedelta(days=NEWS_DAYS)
CURRENT_DATE_STR_NEWS = NEWS_DATE.strftime("%Y-%m-%d")
NEWS_TO_SHOW = 7
NEWSAPI_URL = (f"https://newsapi.org/v2/everything?q=Finance&from={NEWS_DATE}&"
               f"sortBy=popularity&apiKey={env('NEWSAPI_API_KEY')}")


def fetch_data(url):
    response = requests.get(url)
    return response.json()


def get_data_from_apis(urls):
    results = [fetch_data(url) for url in urls]
    return results

def news_view(request):
    urls = [PRIVAT_URL, NEWSAPI_URL]
    raw_data = get_data_from_apis(urls)
    news_articles = raw_data[1]["articles"][::-1]
    view_data = {
        'Date': raw_data[0]['date'],
        'Bank': 'PrivatBank',
        'Exchange_rate': [
            {
                'currency': 'USD',
                'sale': next((rate.get("saleRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'USD'), None),
                'purchase': next((rate.get("purchaseRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'USD'), None)
            },
            {
                'currency': 'EUR',
                'sale': next((rate.get("saleRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'EUR'), None),
                'purchase': next((rate.get("purchaseRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'EUR'), None)
            },
            {
                'currency': 'PLN',
                'sale': next((rate.get("saleRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'PLN'), None),
                'purchase': next((rate.get("purchaseRate") for rate in raw_data[0]["exchangeRate"] if rate.get("currency") == 'PLN'), None)
            }
        ],
        'News': [
            {
                "source": article["source"]["name"],
                "author": article["author"],
                "title": article["title"],
                "description": article["description"],
                "link_to_source": article["url"],
                "publishedAt": article["publishedAt"]
            }
            for article in news_articles[:NEWS_TO_SHOW]
        ]
    }

    return render(request, 'news/index2.html',
                  context={'page_title': 'News and Statistics', 'data': view_data})