import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup


class Core:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Наименование', 'Цена', 'Наличие'])

    async def parse_content(self, session, url: str):
        url = f'{url}'
        async with session.get(url) as response:
            html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        content = soup.findAll('div', class_='product-one__info')
        for product in content:
            name = product.find('span', itemprop='description')
            price = product.find('span', itemprop='price')
            available = True if product.find('span', class_='available_text available') is not None else False
            self.df.loc[len(self.df), self.df.columns] = [
                name.text.strip(),
                price.text.strip() if price is not None else 0,
                available
            ]

    async def run_parse_tasks(self, product_urls: list[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [self.parse_content(session, url) for url in product_urls]
            await asyncio.gather(*tasks)
            return self.df
