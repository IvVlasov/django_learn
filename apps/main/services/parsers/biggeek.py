import requests
from bs4 import BeautifulSoup
from .product import ProductTuple


BIG_GEEK_URL = 'https://biggeek.ru'

CLASS_NAMES = {
    'price': 'total-prod-price',
    'photo_url': 'cart-modal-image',
    'description': 'tabs-content__inner',
    'vendor_cont': 'tabs-content__txt-row',
}


def parse_big_geek(category_url: tuple) -> str | list[ProductTuple]:
    """
    Parse ONLY FIRST page of category
    """
    try:
        links = _get_products_hrefs(category_url)
    except ValueError as e:
        return e
    except ConnectionError as e:
        return e

    if not links:
        return 'Страница католога не смогла загрузиться'

    try:
        products = _get_products_data(links)
    except ValueError as e:
        return e
    except ConnectionError as e:
        return e
    return products


def _get_products_hrefs(category_href: str) -> list[str]:
    url = BIG_GEEK_URL + category_href
    r = requests.get(url)

    if r.status_code != 200:
        raise ConnectionError('Страница католога не найдена')

    soup = BeautifulSoup(r.text, 'html.parser')
    catalog_cards = soup.find_all('div', {'class': 'catalog-card'})

    if not catalog_cards:
        raise ValueError('Страница католога не смогла загрузиться')

    links = []
    for el in catalog_cards[:-1]:
        link = el.find('a', {'class': 'catalog-card__title'})
        if link:
            links.append(link['href'])
    return links


def _get_products_data(links: list[str]) -> list[ProductTuple]:
    products = []
    for link in links:
        data = _get_product_data(link)
        products.append(data)
    return products


def _get_product_data(path: str) -> ProductTuple:
    url = BIG_GEEK_URL + path
    resp = requests.get(url)
    if not resp.status_code == 200:
        raise ConnectionError('Страница товара не смогла загрузиться')

    product_page = BeautifulSoup(resp.text, 'html.parser')
    try:
        name = product_page.find('h1').text
        price = product_page.find(
            'span', {'class': CLASS_NAMES['price']}
        ).text
        photo_url = 'https:' + product_page.find(
            'img', {'class': CLASS_NAMES['photo_url']}
        )['src']
        description = product_page.find(
            'div', {'class': CLASS_NAMES['description']}
        ).text
        vendor_code = product_page.find(
            'div', {'class': CLASS_NAMES['vendor_cont']}
        ).find('p', {'class': 'value'}).text

    except ValueError:
        raise ValueError('Страница товара не смогла загрузиться')

    return ProductTuple(description, price, photo_url, vendor_code, name)
