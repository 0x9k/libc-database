# -*-coding:utf-8-*-
__author__ = 'joker'

import requests
from bs4 import BeautifulSoup
import commands

headers = {'content-type': 'text/html',
           'Connection': 'close',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
url = "http://security.ubuntu.com/ubuntu/pool/main/g/glibc/"
r = requests.get(url, allow_redirects=True, headers=headers, stream=True, )
text = r.text

soup = BeautifulSoup(text)
a_all = soup.find_all("a")

base_url = "http://security.ubuntu.com/ubuntu/pool/main/g/glibc/"

for a in a_all:
    href = a.get("href")
    if "libc6" in href:
        _, _ = commands.getstatusoutput("wget {0}".format(base_url + href))
