import requests
from bs4 import BeautifulSoup
import pandas as pd

import datetime
str = '(Submitted on 23 Oct 2019)'
str = str.replace('(Submitted on ','').rstrip(')')
date = datetime.datetime.strptime(str, '%d %b %Y')

print(date)
