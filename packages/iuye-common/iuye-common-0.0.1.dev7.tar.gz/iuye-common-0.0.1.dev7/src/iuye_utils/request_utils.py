import requests
import random

userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'

header = {
    'User-Agent': userAgent
}


def get(url):
    return requests.get(url, headers=header,  timeout=3)
