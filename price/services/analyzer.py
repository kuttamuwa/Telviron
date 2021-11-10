from celery import shared_task

# @shared_task
from price.services.searcher import Searcher


def find_top_50_drops():
    coins = Searcher.coins.filter_drop(value=50)