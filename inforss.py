#!/usr/bin/env python3

import pycurl
from io import BytesIO
import xml.etree.ElementTree as ET

with open('key') as file:
	KEY = file.read().rstrip()

RSS_URL = "http://www.tagesschau.de/xml/rss2"
INFOBEAMER_URL = "https://info-beamer.com/api/v1/setup/4972"

rssbuffer = BytesIO()
postbuffer = BytesIO()

### Get news articles from rss feed
curl =  pycurl.Curl()
curl.setopt(curl.URL, RSS_URL)
curl.setopt(curl.WRITEDATA, rssbuffer)
curl.perform()
del curl

### Parse into info-beamer format (json)
tree = ET.fromstring(rssbuffer.getvalue().decode('utf8'))
news = []
for item in tree.findall("*/item")[0:4]:
	news.append('{"text":"' + item.find("description").text + '"}')

data = 'config={"scroller":{"texts":['
data += str.join(',', news)
data += ']}}&mode=update'


### curl curly data into fluffy clouds
curl = pycurl.Curl()
curl.setopt(curl.URL, INFOBEAMER_URL)
curl.setopt(curl.USERPWD, ":" + KEY)
curl.setopt(curl.POST, 1)
curl.setopt(curl.POSTFIELDS, data.encode('utf-8'))
curl.setopt(curl.WRITEDATA, postbuffer)
curl.perform()
del curl
print(postbuffer.getvalue())
