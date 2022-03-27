import requests
import csv
from bs4 import BeautifulSoup as soup

if __name__ == '__main__':

    site = "https://www.zoopla.co.uk"
    for_sale = "for-sale/property"
    city = "oxford"

    page = requests.get(f"{site}/{for_sale}/{city}")
    print(page.status_code)

    bsobj = soup(page.content, 'html.parser')

    total_results = bsobj.select('p[class*="SearchResultsTotalText"]')
    total_results = int(total_results[-1].get_text().split()[0])
    print(f"{total_results} results")

    pagination_numbers = bsobj.select('li[class*="PaginationItemNumber"]')
    npages = int(pagination_numbers[-1].get_text())
    print(f"Number of pages {npages}")

    listings = []

    for page_number in range(2, npages + 1):
        page = requests.get(f"{site}/{for_sale}/{city}/?pn={page_number}")

        if page.status_code == 200:
            bsobj = soup(page.content, 'html.parser')

            for l in bsobj.select('div[id*="listing_"]'):

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
                listings.append(listing)

    with open('../output/listings.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, listings[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(listings)
