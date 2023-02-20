import requests

from bs4 import BeautifulSoup as bs
import time
from models import Models
from alchemy import session


class Parsing():

    def __init__(self, url: str):
        self.url = url


    @staticmethod
    def page(number):
        return f'/b-apartments-condos/page-{number}/city-of-toronto/c37l1700273'


    def soup(self, url: str) -> bs:
        headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
        time.sleep(5)
        response = requests.get(url, headers=headers)
        return bs(response.text, 'lxml')


    @property
    def get_total_pages(self) -> int:
        soup = self.soup(self.url + self.page(1))
        res = soup.find('span', {'class': 'resultsShowingCount-1707762110'}).text.split() 
        pages = int(res[5]) / int(res[3])

        if int(pages) == pages:
            return int(pages)
        return int(pages) + 1



    @staticmethod
    def image(soup:bs)->str:
    
        try:
            image = soup.find('div', {'class': 'mainImage'}).find('img').get('src')
            # print(image)
        except:
            image = ''


    @staticmethod
    def date_format(source: list) -> str:
        months = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
            'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11','December': '12'
        }
        day = source[1][:-1] 

        if len(day) == 1:
            day = '0' + day

        month = months[source[0]]
        year = source[2]
        return f'{day}-{month}-{year}'


    def time(self, soup: bs) -> str:
        date_container = soup.find('div', {'class': 'datePosted-383942873'})

        try:
            source = date_container.find('time').get('title').split()
        except AttributeError:
            pass
        else:
            return self.date_format(source)

        try:
            source = date_container.find('span').get('title').split()
        except AttributeError:
            return None
        else:
            return self.date_format(source)


    @staticmethod
    def price_va(soup: bs) -> dict:
        try:
            currency_and_price = soup.find('div', {'class': 'priceWrapper-1165431705'}).find('span').text
        except:
            currency_and_price = ''


    def ads(self, soup: bs, number: int):

        for md in soup.find_all('div', {'class': 'info'}):
            uri = md.find('a', {'class': 'title'}).get('href')
            soup = self.soup(self.url + uri)
            image = self.image(soup)
            date = self.time(soup)
            currency_and_price = self.price_va(soup)
            currency = currency_and_price.get('currency')
            price = currency_and_price.get('price')
            data = Models(page=number, image=image, date=date, currency=currency, price=price)
            session.add(data)
            session.commit()
        
    
    def parse(self):
        ads = session.query(Models).all()

        for md in ads:
            session.delete(md)
        
        session.commit()

        for number in range(1, self.last_page+1):
            url = self.url + self.page(number)
            soup = self.soup(url)
            self.ads(soup, number)


parsing = Parsing('https://www.kijiji.ca')

parsing.parse()
