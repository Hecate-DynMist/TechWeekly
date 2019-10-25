import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://arxiv.org/list/cs.LG/recent'
RESPONSE=requests.get(url)
SOUP=BeautifulSoup(RESPONSE.text, 'html.parser')

print(SOUP)
