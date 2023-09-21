import json

global data

#bangkok, chanthaburi, Chiang Mai, Chiang Rai, Krabi, Nong Khai, Phuket
file_to_attach = 'turkey-hotels-in-hethiye.json'

with open('output/' + file_to_attach, 'r') as f:
  data = json.load(f)

try:
    open('./sites.txt', 'w').close()
except IOError:
    print('Failure')

for el in data:
  if (el['website'] != None):
    file = open('./sites.txt', 'a', encoding='utf-8')
    file.write(el['website'] + '\n')