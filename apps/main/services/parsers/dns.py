from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from .product import ProductTuple
import os
import time


def parse_dns(category_url: str) -> list[ProductTuple]:
    products_info = []
    driver = _create_firefox_driver()
    driver.get('https://www.dns-shop.ru' + category_url)

    products = driver.find_elements(By.CLASS_NAME, 'catalog-product')
    products_urls = []
    for product in products:
        url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        products_urls.append(url)

    for product_url in products_urls:
        try:
            product_info = _get_product_data(driver, product_url)
        except NoSuchElementException:
            driver.quit()
            return 'Элемент не на странице не найден'
        products_info.append(product_info)

    driver.quit()
    return products_info


def _create_firefox_driver() -> Firefox:
    options = Options()
    options.headless = True
    s = Service(executable_path=os.getcwd() + '/drivers/geckodriver')
    profile = FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    driver = Firefox(firefox_profile=profile, service=s, options=options)
    return driver


def _get_product_data(driver: Firefox, product_url: str) -> ProductTuple:
    driver.get(product_url)
    time.sleep(3)

    description = driver.find_element(
        By.CLASS_NAME, 'product-card-description-text'
    ).text

    price = driver.find_element(
        By.CLASS_NAME, 'product-buy__price'
    ).text.split('₽')[0]

    photo_url = driver.find_element(
        By.CLASS_NAME, 'product-images-slider__main-img'
    ).get_attribute('src') + '.webp'

    vendor_code = driver.find_element(
        By.CLASS_NAME, 'product-card-top__code'
    ).text.replace('Код товара: ', '')

    name = driver.find_element(
        By.CLASS_NAME, 'product-card-top__title'
    ).text
    return ProductTuple(description, price, photo_url, vendor_code, name)
