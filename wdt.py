## This is a test comment for git commit 1
import requests
import urllib.request
from datetime import datetime
import time
from bs4 import BeautifulSoup
import os

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
myfile = "/home/mgmtadmin/wdt/wdt-" + dt_string
f = open(myfile, "w")
f.write("Subject:"+word+"\n"+message+"\n")
f.close()
sendmail = '/usr/sbin/sendmail croiset.eric@gmail.com < ' + myfile
os.system(sendmail)
