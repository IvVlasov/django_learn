from django.conf import settings

from main.services.parsers.dns import parse_dns
from main.services.parsers.biggeek import parse_big_geek
from main.services.parsers.product import ProductTuple
from shop.services.image import load_photo
from shop.models import Product, Category
from main.models import Parser


def parse_all(params: dict) -> dict[str, str] | None:
    result = 'Парсинг закончен, результаты: '
    counter = 0
    for param in params:
        if param['site_name'] == Parser.BIGGEEK:
            products = parse_big_geek(param['url_slug'])

        elif param['site_name'] == Parser.DNS:
            products = parse_dns(param['url_slug'])
        else:
            return

        if isinstance(products, str):
            result += f'Ошибка при обработке {param["cat_name"]} \
                    Info: {products}',
            continue

        insert_data(products, param)
        counter += len(products)

    result += f'Всего товаров спаршено: {counter}'
    return {
        'code': 'success',
        'message': result,
    }


def insert_data(products: list[ProductTuple], params: dict[str, str]) -> None:
    '''Insert products data into database'''

    category_obj = Category.objects.get_or_create(
        name=params['cat_name'], slug=params['cat_slug']
    )

    for product in products:
        color = ''
        name = product.name
        if params['type'] == 'phone':
            color = product.name.split('(')[-1][:-1]
            name = '('.join(product.name.split('(')[:-1])

        if params['site_name'] == Parser.DNS:
            color = product.name.split()[-1]
            name = ' '.join(product.name.split()[:-1])

        price = int(product.price.replace(' ', '')) * settings.PRICE_MULTIPLIER

        prod = Product.objects.filter(vendor_code=product.vendor_code,
                                      name=name)
        if prod:
            prod.update(
                description=product.description,
                price=price,
            )
            continue
        else:
            photo = load_photo(product.photo_url)
            Product.objects.get_or_create(
                vendor_code=product.vendor_code,
                name=name,
                color=color,
                photo=photo,
                description=product.description,
                category=category_obj[0],
                price=price,
            )
