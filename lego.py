from model import LegoManager
legoManager = LegoManager("https://www.lego.com/zh-cn/service/buildinginstructions")
# legoManager.get_themes('themes.csv')
legoManager.load_themes('themes.csv')
legoManager.get_products('products.csv')
