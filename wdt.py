import requests
import urllib.request
from datetime import datetime
import time
from bs4 import BeautifulSoup
import os
#Wort des Tages Duden Crawler mit Cronjob 0 8 * * * /usr/bin/python3 /home/mgmtadmin/wdt/wdt.py
#Sendmail with Iptables block Ports 25 587
#class="scene__title-link"

url = 'https://www.duden.de/wort-des-tages'
response = requests.get(url)
#print(soup.prettify())
soup = BeautifulSoup(response.text, 'html.parser')
word = {}
wordexp = {}
for a in soup.findAll('a', {'class': 'scene__main'}):
        wordexp = a.text.strip()
for a in soup.findAll('a', {'class': 'scene__title-link'}):
        word = a.text.strip()
message = word + ' - ' + wordexp

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
myfile = "wdt-" + dt_string

f = open(myfile, "w")
f.write("Subject:"+word+"\n"+message+"\n")
f.close()

sendmail = 'sendmail croiset.eric@gmail.com < /home/mgmtadmin/wdt/' + myfile
os.system(sendmail)
