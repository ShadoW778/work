from selenium import webdriver
import time
import re
import requests
from urllib.parse import urlparse
import vlc

PATH = 'C:\chromedriver\chromedriver.exe'

theme = input('Введите тему поиска (она будет отображена в файле emails.txt)... ')

file = open('./emails.txt', 'a', encoding='utf-8')
file.write('\n\n\n' + theme + '\n')

l=list()
o={}

global urlsScraped
global target_urls
global GLOBAL_URLS_CHECKED
global GLOBAL_SUBURLS_CHECKED
GLOBAL_URLS_CHECKED = 0
GLOBAL_SUBURLS_CHECKED = 0
target_urls = []

with open('./urlsScraped.txt') as f:
   urlsScraped = f.read().splitlines()

with open('./urls.txt') as f:
   notParsed = f.read().splitlines()

for url in notParsed:
   el = urlparse(url).netloc
   if url.startswith('https'):
      el = 'https://' + el + '/'
   else:
      el = 'http://' + el + '/'
   if (el == 'instagram.com'):
      print('Deleting url - ' + url)
      file = open('./instagrams.txt', 'a', encoding='utf-8')
      file.write(url + '\n') 
      notParsed.remove(url)
   if el == 'facebook.com':
      # page_name = url.split('https://www.facebook.com/')[1].split('/')[0]
      # el = 'https://www.facebook.com/' + page_name + '/'
      print('Deleting url - ' + url)
      file = open('./facebooks.txt', 'a', encoding='utf-8')
      file.write(url + '\n') 
      notParsed.remove(url)
   target_urls.append(el)

res = list(set(urlsScraped) & set(target_urls))

if len(res) > 0:
    print('Already used url(s) detected')
    for i in range(0, len(res)):
        print('Deleting url - ' + res[i])
        target_urls.remove(res[i])

email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"


# working piece

print('Соединяюсь с Chromium...\nПодготовка к выполнению')

driver=webdriver.Chrome(PATH)
global globalEmails
globalEmails = []

for url in target_urls:
   print('... просыпаюсь и обрабатываю - ' + url)
   try:
      response = requests.get(url)
      if response.status_code == 200:
         driver.get(url)
         html = driver.page_source
         emails = re.findall(email_pattern, html)

         if (not 'facebook.com' in url):
            subpages = []

            response = requests.get(url + 'contacts/')
            if response.status_code == 200:
               print(url + 'contacts/ - this page exists. Parsing...')
               subpages.append(url + 'contacts/')
   
   
            response = requests.get(url + 'contact-us/')
            if response.status_code == 200:
               print(url + 'contact-us/ - this page exists. Parsing...')
               subpages.append(url + 'contact-us/')

            response = requests.get(url + 'kontakt/')
            if response.status_code == 200:
               print(url + 'kontakt/ - this page exists. Parsing...')
               subpages.append(url + 'kontakt/')
   
            print('Парсинг подстраниц...')
            for suburl in subpages:
               driver.get(suburl)
               html = driver.page_source
               emails = emails + re.findall(email_pattern, html)
               GLOBAL_SUBURLS_CHECKED += 1
         

         file = open('./urlsScraped.txt', 'a', encoding='utf-8')
         file.write(url + '\n')
         globalEmails = globalEmails + emails

         print(url + ' - сайт был обработан. Засыпаю...')
         GLOBAL_URLS_CHECKED += 1
         emails = list(set(emails))
         for em in emails:
            file = open('./emails.txt', 'a', encoding='utf-8')
            file.write(em + '\n')
         time.sleep(3)
      else:
         print("The website ain't response")
         file = open('./urlsScraped.txt', 'a', encoding='utf-8')
         file.write(url + '\n')
         p = vlc.MediaPlayer("./error.mp3")
         p.play()
   except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, requests.exceptions.InvalidChunkLength):
      print("The website ain't response")
      p = vlc.MediaPlayer("./error.mp3")
      p.play()
      file = open('./urlsScraped.txt', 'a', encoding='utf-8')
      file.write(url + '\n')



finalEmails = list(set(globalEmails))
print(finalEmails)
print('Успешная работа. ' + str(len(finalEmails)) + ' сохраненных почт(ы). ' + str(GLOBAL_URLS_CHECKED) + ' сайтов + ' + str(GLOBAL_SUBURLS_CHECKED) + ' обработанных подсайтов')

file = open('./urlsScraped.txt', 'a', encoding='utf-8')
file.write(str(len(finalEmails)) + '\n')

driver.close()

p = vlc.MediaPlayer("./complete.mp3")
p.play()