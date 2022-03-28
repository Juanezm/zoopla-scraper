import requests
from bs4 import BeautifulSoup
import csv


class ZooplaScraper:

    def __init__(self, url="https://www.zoopla.co.uk", interest="for-sale/property", city="oxford"):
        self.url = f"{url}/{interest}/{city}"
        self.html = None
        self.total_results = None
        self.total_pages = None
        self.listings = []

    def __download_html(self, path=''):
        try:
            r = requests.get(self.url + '/' + path)
            r.raise_for_status()
            return r.content
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def __get_total_results(self, main_soup):
        total_results = main_soup.select_one('p[class*="SearchResultsTotalText"]')
        self.total_results = int(total_results.get_text().split()[0])

    def __get_total_pages(self, main_soup):
        pagination_numbers = main_soup.select('li[class*="PaginationItemNumber"]')
        self.total_pages = int(pagination_numbers[-1].get_text())

    def __scrape_listings(self, soup):
        for l in soup.select('div[id*="listing_"]'):
            listing = {
                'agency': l.select_one('a[class*="AgencyLogoLink"]').attrs['href'].split('/')[-2],
                'price': l.select_one('p[class*="Price "]').text,
                'title': l.select_one('h2[class*="AddressTitle "]').text,
                'address': l.select_one('p[class*="Address "]').text,
                'date': l.select_one('div[class*="DateDetail"]').text,
                'transport': [],
            }

            features = l.select_one('div[class*="WrapperFeatures"]')
            for f in features.select('div[class*="IconAndText"]'):
                listing[f.select_one('span[class*="StyledIcon"]').attrs['data-testid']] = \
                    f.select_one('p[class*="Text "]').text

            transport = l.select_one('div[class*="TransportWrapper"]')
            for t in transport.select('div[class*="IconAndText"]'):
                if not t.attrs.get('data-testid'):
                    listing['transport'].append(
                        t.select_one('p[class*="Text "]').text
                    )

            print(listing)
            self.listings.append(listing)

    def to_csv(self, output):
        with open(output, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, self.listings[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.listings)

    def scrape(self):

        html = self.__download_html()
        soup = BeautifulSoup(html, 'html.parser')

        self.__get_total_results(soup)
        self.__get_total_pages(soup)

        self.__scrape_listings(soup)

        for page_number in range(2, self.total_pages + 1):

            html = self.__download_html(path=f"/?pn={page_number}")
            soup = BeautifulSoup(html, 'html.parser')

            self.__scrape_listings(soup)

        if len(self.listings) == self.total_results:
            print("All listings have been downloaded successfully")
        else:
            print("Some listings have not been downloaded for some reason")

