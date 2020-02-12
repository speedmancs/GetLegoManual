import os


class Product:
    def __init__(self, product_id, name, pdf_locations, images, theme, theme_name, launch_year, folder):
        self.product_id = product_id
        self.name = name
        self.pdf_locations = pdf_locations
        self.images = images
        self.theme = theme
        self.launch_year = launch_year
        self.theme_name = theme_name
        self.local_pdfs = ['{}\\{}'.format(folder, os.path.basename(path)) for path in pdf_locations]
        self.local_images = ['{}\\{}'.format(folder, os.path.basename(path)) for path in images]

    def write(self, file, newline=True):
        for (pdf, lpdf, image, limage) in zip(self.pdf_locations, self.local_pdfs, self.images, self.local_images):
            items = [self.product_id, self.name, self.theme_name, self.theme, str(self.launch_year), pdf, lpdf, image, limage]
            file.write(','.join(items))
            if newline:
                file.write('\n')
