import os
import requests
import time
from util import StrUtil


class Product:
    def __init__(self, product_id, name, pdf_locations, images, theme, theme_name, launch_year, store_folder):
        self.product_id = product_id
        self.name = name
        self.pdf_locations = pdf_locations
        self.images = images
        self.theme = theme
        self.launch_year = launch_year
        self.theme_name = theme_name
        self.store_folder = store_folder

    def write(self, file):
        for (pdf, image) in zip(self.pdf_locations, self.images):
            file.write(','.join([self.product_id, self.name, self.theme_name, self.theme, str(self.launch_year), pdf, image]))
            file.write('\n')

    def download(self):
        resources = self.pdf_locations + self.images
        for resource in resources:
            basename = StrUtil.get_base(os.path.basename(resource))
            local_folder = os.path.join(self.store_folder, StrUtil.filter(self.theme_name), StrUtil.filter(self.name))
            if not os.path.isdir(local_folder):
                os.makedirs(local_folder)
            local_path = os.path.join(local_folder, basename)
            if os.path.exists(local_path):
                print(f'resource {basename} has been downloaded')
                continue

            try:
                with requests.get(resource, stream=True) as r:
                    r.raise_for_status()
                    with open(local_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except:
                print(f'failed to download {basename}')

            print(f'downloaded {basename} to {local_path}')
            time.sleep(0.2)


