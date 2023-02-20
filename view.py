from alchemy import session
from models import Models

ads = session.query(Models).filter(Models.page==1)
for md in ads:
    print(f'изображение: {md.image}')
    print(f'дата: {md.date}')
    print(f'цена: {md.currency}{md.price}')

