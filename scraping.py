from urllib.request import urlopen, Request, urlretrieve
from urllib.error import URLError, HTTPError
from handle_html import handle_html
from bs4 import BeautifulSoup
import pandas as pd

response = urlopen('https://alura-site-scraping.herokuapp.com/index.php?page=1')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

#taking the number of pages to scrap
number_of_pages = int(str(soup.find('span', {'class':'info-pages'})).split('<')[1].split(' ')[-1])

#variables to store information
cards = []

#function that receives a card and extract its information
def getCardData(ad):
    card = {}

    #one ad information (car value, name, date, location ...)
    #ad = soup.find('div', {'class' : 'well card'})

    #--
    card['value'] = ad.find('p', {'class': 'txt-value'}).get_text()

    #---
    otherInfos = ad.find('div', {'class':'body-card'}).find_all('p')
    for info in otherInfos:
        card[info.get('class')[0].split('-')[-1]] = info.get_text()

    #--
    items = ad.find('div', {'class', 'body-card'}).ul.find_all('li')
    items.pop()
    acessories = []
    for item in items:
        acessories.append(item.get_text().replace('► ', ''))
    card['items'] = acessories

    #saving an ad image in output/images
    image = ad.find('div', {'class': 'image-card'}).img
    urlretrieve(image.get('src'), './output/images/' + image.get('src').split('/')[-1])

    return card


for i in range(number_of_pages):
    response = urlopen('https://alura-site-scraping.herokuapp.com/index.php?page='+ str(i + 1))
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    ads = soup.find('div', {'id': 'container-cards'}).find_all('div', {'class': 'well card'})

    for ad in ads:
        cards.append(getCardData(ad))

print(cards)

dataset = pd.DataFrame(cards)
dataset.to_csv('./output/dataset.csv', sep=';', index=False, encoding='utf-8-sig')
