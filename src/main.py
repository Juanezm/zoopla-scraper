from src.scraper import ZooplaScraper


if __name__ == '__main__':
    zs = ZooplaScraper()
    zs.scrape()
    zs.to_csv('../output/listings.csv')
