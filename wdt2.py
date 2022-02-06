import requests
import urllib.request
from datetime import datetime
import time
from bs4 import BeautifulSoup
import os

#class="scene__title-link"
#scene__title-link


url = 'https://www.duden.de/wort-des-tages'
response = requests.get(url)
#print(soup.prettify())
soup = BeautifulSoup(response.text, 'html.parser')
urls = []
word = {}
wordexp = {}
for h in soup.findAll('a', {'class': 'scene__title-link'}):
        try:
                if 'href' in h.attrs:
                        url = h.get('href')
                        urls.append(url)
        except:
                pass
for url in urls:
        wdt = 'https://www.duden.de' + url
        response2 = requests.get(wdt)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        for span in soup2.findAll('span', {'class': 'lemma__main'}):
                word = span.text.strip()
        table = soup2.findAll('div', {'id': 'bedeutung'})
        for x in table:
                wordexp = x.find('p').text
print (wordexp)
print (word)


tword = ''.join(filter(str.isalnum, word))
print (tword)

message = word + ' - ' + wordexp
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
myfile = "/home/mgmtadmin/wdt/wdt-" + dt_string
f = open(myfile, "w")
#f.write("Subject: WDT "+word+"\n"+wordexp+"\n")
f.write("Content-Type: text/plain; charset=utf-8\r\nFrom: root@slave.ercro.tech\r\nSubject: WDT "+tword+"\r\n\r\n"+wordexp)
f.close()
sendmail = '/usr/sbin/sendmail croiset.eric@gmail.com < ' + myfile
os.system(sendmail)
