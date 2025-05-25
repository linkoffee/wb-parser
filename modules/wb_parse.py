import requests
from typing import Optional

from modules.settings import settings


def get_wb_info(article: str) -> Optional[dict]:
    """ Получает информацию о товаре с Wildberries по его артикулу """
    api_data = fetch_api_data(article)
    if not api_data:
        return None

    return extract_product_data(api_data)


def fetch_api_data(article: str) -> Optional[dict]:
    """ Выполняет запрос к API Wildberries и возвращает сырые данные """
    api_url = f"https://card.wb.ru/cards/detail?&dest=-1257786&nm={article}"

    try:
        response = requests.get(
            api_url,
            headers=settings.HEADERS,
            timeout=settings.TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def extract_product_data(api_data: dict) -> Optional[dict]:
    """ Извлекает данные о товаре из ответа API Wildberries """
    products = api_data.get("data", {}).get("products", [])

    if not products:
        return None

    product = products[0]
    price = int(product.get("priceU", 0)) / 100

    product_data = {
        "product_name": product.get("name"),
        "product_price": f"{price:.2f} ₽",
    }

    return product_data
