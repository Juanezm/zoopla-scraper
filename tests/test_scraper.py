import pytest
from bs4 import BeautifulSoup

from src.scraper import ZooplaScraper


def test_download_html_default():
    zs = ZooplaScraper()
    page = zs._ZooplaScraper__download_html()
    assert page


def test_download_html_not_found():
    zs = ZooplaScraper(url="FakeUrl")
    with pytest.raises(Exception):
        zs._ZooplaScraper__download_html()


def test_get_total_results():
    zs = ZooplaScraper()
    html = zs._ZooplaScraper__download_html()
    soup = BeautifulSoup(html, 'html.parser')
    zs._ZooplaScraper__get_total_results(soup)

    assert zs.total_results


def test_get_total_pages():
    zs = ZooplaScraper()
    html = zs._ZooplaScraper__download_html()
    soup = BeautifulSoup(html, 'html.parser')
    zs._ZooplaScraper__get_total_pages(soup)

    assert zs.total_pages


def test_scrape():
    zs = ZooplaScraper()
    zs.scrape()

    assert zs.listings


def test_to_csv():
    zs = ZooplaScraper()
    zs.scrape()
    zs.to_csv('../output/listings.csv')
