import argparse
from model import LegoManager
from config import LegoConfig
from util import FileUtil


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Lego management')
    args.add_argument('--split', dest='split_products', action='store_true')
    args.add_argument('-n', type=int, dest='split_num')
    args.add_argument('--fetch_themes', dest='fetch_themes', action='store_true')
    args.add_argument('--fetch_products', dest='fetch_products', action='store_true')
    args.add_argument('--download', dest='download', action='store_true')
    args.add_argument('-i', '--input', type=str, dest='input', help="input file")
    args.add_argument('-o', '--output', type=str, dest='output', help="output file")
    args.add_argument("-s", '--store', type=str, dest="store", help="root store folder")
    args = args.parse_args()
    if args.split_products:
        FileUtil.split(args.input, args.split_num)
    elif args.fetch_themes:
        legoManager = LegoManager(LegoConfig.main_page, None)
        legoManager.get_themes(args.output)
    elif args.fetch_products:
        legoManager = LegoManager(LegoConfig.main_page, None)
        legoManager.load_themes(args.input)
        legoManager.get_products(args.output)
    elif args.download:
        legoManager = LegoManager(None, args.store)
        legoManager.load_products(args.input)
        legoManager.download()
        pass



