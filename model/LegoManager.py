import urllib.request
from bs4 import BeautifulSoup
import json
import os
import time
from model import Product
from util import FileUtil
from config import LegoConfig


class LegoManager:
    def __init__(self, main_page_url, store_folder):
        self.main_page_url = main_page_url
        self.themes = []
        self.products = []
        self.store_folder = store_folder

    def get_themes(self, output_file):
        response = urllib.request.urlopen(self.main_page_url)
        content = response.read().decode('utf-8')

        soup = BeautifulSoup(content, 'lxml')
        search_element = soup.find("div", attrs={"class": "product-search"})
        data = search_element.attrs['data-search-themes']
        themes = json.loads(data)
        FileUtil.writelines(output_file, [f"{item['Label']},{item['Key']}" for item in themes])

    def load_themes(self, theme_file):
        self.themes = FileUtil.load_csv(theme_file)

    def load_products(self, products_file):
        items = FileUtil.load_csv(products_file)
        for pid, name, tname, tid, year, pdf, image in items:
            self.products.append(Product(product_id=pid, name=name, theme=tid, store_folder=self.store_folder,
                                         theme_name=tname, launch_year=year, pdf_locations=[pdf], images=[image]))

    def download(self):
        for product in self.products:
            product.download()

    def get_products(self, output_file):
        for label, key in self.themes:
            folder = os.path.join(self.store_folder, label)
            self.fetch_products(folder, key)

        with open(output_file, mode='w', encoding='utf-8') as file:
            for product in self.products:
                product.write(file)

    def fetch_and_parse(self, url):
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        return json.loads(content)

    def fetch_products(self, folder, key):
        index = 0
        finished = False
        total = 0
        while not finished:
            url = LegoConfig.url_template.format(LegoConfig.search_url, index, key)
            data = self.fetch_and_parse(url)
            cnt = int(data["count"])
            time.sleep(0.2)
            total += cnt
            print('{} items fetched for theme {}, total: {}'.format(cnt, key, total))
            if cnt < 10:
                finished = True
            else:
                index += 10

            try:
                self.add_products(data["products"], folder, key)
            except KeyError:
                print("Failed to fetch products for {}".format(url))

    def add_products(self, products, folder, theme):
        for product in products:
            pdfs = [instruction["pdfLocation"] for instruction in product["buildingInstructions"]]
            front_pages = [instruction["frontpageInfo"] for instruction in product["buildingInstructions"]]
            self.products.append(Product(product_id=product["productId"], name=product["productName"],
                                         pdf_locations=pdfs, images=front_pages,
                                         theme=theme, store_folder=folder,
                                         theme_name=product["themeName"],
                                         launch_year=product["launchYear"]))