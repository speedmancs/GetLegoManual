import urllib.request
from bs4 import BeautifulSoup
import json
import os
import time
from model import Product


class LegoManager:
    def __init__(self, main_page_url):
        self.main_page_url = main_page_url
        self.themes = []
        self.products = []

    def get_themes(self, output_file):
        response = urllib.request.urlopen(self.main_page_url)
        content = response.read().decode('utf-8')

        soup = BeautifulSoup(content, 'lxml')
        search_element = soup.find("div", attrs={"class": "product-search"})
        data = search_element.attrs['data-search-themes']
        themes = json.loads(data)

        with open(output_file, mode='w', encoding='utf-8') as file:
            lines = ["{},{}".format(item['Label'], item['Key']) for item in themes]
            file.writelines('\n'.join(lines))

    def load_themes(self, theme_file):
        with open(theme_file, mode='r', encoding='utf-8') as file:
            for item in file.readlines():
                label, key = item.rstrip().split(',')
                self.themes.append((label, key))

    def get_products(self, output_file):
        for label, key in self.themes:
            folder = '.\\store\\{}'.format(label)
            if not os.path.isdir(folder):
                os.makedirs(folder)
            self.fetch_products(folder, key)

        print(len(self.products))
        with open(output_file, mode='w', encoding='utf-8') as file:
            for product in self.products:
                product.write(file)

    def fetch_and_parse(self, url):
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        return json.loads(content)

    def fetch_products(self, folder, key):
        index = 0
        search_url = 'https://www.lego.com//service/biservice/searchbytheme'
        url_template = '{}?fromIndex={}&onlyAlternatives=false&theme={}'
        finished = False
        total = 0
        while not finished:
            url = url_template.format(search_url, index, key)
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
                                         theme=theme, folder=folder,
                                         theme_name=product["themeName"],
                                         launch_year=product["launchYear"]))