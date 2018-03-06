#!/usr/bin/env python3

import pycurl
from io import BytesIO
import xml.etree.ElementTree as ET

with open('key') as file:
	KEY = file.read()

print(KEY)
RSS_URL = "http://www.tagesschau.de/xml/rss2"

buffer = BytesIO()

curl = pycurl.Curl()
curl.setopt(curl.URL, RSS_URL)
curl.setopt(curl.WRITEDATA, buffer)
curl.perform()

#print(buffer.getvalue().decode('utf8'))

tree = ET.fromstring(buffer.getvalue().decode('utf8'))
for item in tree.findall("*/item")[0:4]:
	print(item)

