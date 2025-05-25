# ТЗ: парсинг с Wildberries
Написать Python-скрипт, содержащий следующую функцию:

```py
def get_wb_info(article: str) -> Optional[dict]:
...
```

Данная функция принимает артикул товара Wildberries (например, `400682365`) и возвращает словарь с названием и ценой товара.
Если товар по данному артикулу не найден, верните None.

Условия:
- Разрешается выполнить парсинг только на запросах (urllib, requests, aiohttp и т.п.), без использования решений типа Selenium
- Необязательно писать всю логику в рамках одной функции. Приветствуется чистый и структурированный код.
- Приложите краткое пояснение к тому, как вы выполнили задание.

# Пояснение:
1. Для начала мне нужно было реализовать логику поиска информации по конкретному товару, используя `API Wildberries`:
```py
api_url = f"https://card.wb.ru/cards/detail?&dest=-1257786&nm={article}"  # Где article - уникальный ID товара
```
Таким образом можно получить и перехватить любую информацию о товаре в формате `json`:
```json
{"state":0,"params":{"version":1,"curr":"rub","payloadVersion":1},"data":{"products":[{"id":216157923,"root":218540346,"kindId":0,"brand":"ARTVILS","brandId":508542,"siteBrandId":0,"colors":[{"name":"белый","id":16777215},{"name":"красный","id":16711680},{"name":"розовый","id":16761035},{"name":"зеленый","id":32768},{"name":"голубой","id":11393254}],"subjectId":4152,"subjectParentId":1284,"name":"Эпоксидная смола набор для творчества с УФ-лампой","entity":"","matchId":170694482,"supplier":"ARTVILS - вдохновение для семейного творчества","supplierId":143823,"supplierRating":4.9,"supplierFlags":16,"priceU":182400,"salePriceU":87500,"logisticsCost":2000,"sale":0,"returnCost":0,"diffPrice":false,"saleConditions":134217728,"pics":13,"rating":5,"reviewRating":4.9,"nmReviewRating":4.9,"feedbacks":16415,"nmFeedbacks":16415,"panelPromoId":1001365,"promoTextCard":"РАСПРОДАЖА","promoTextCat":"РАСПРОДАЖА","volume":20,"viewFlags":1056792,"promotions":[63484,155232,188238,188695,190352,190353,1001365],"sizes":[{"name":"","origName":"0","rank":0,"optionId":344624137,"returnCost":0,"stocks":[{"wh":507,"dtype":4,"dist":106,"qty":84,"priority":92959,"time1":3,"time2":26},{"wh":321932,"dtype":4,"dist":77,"qty":1,"priority":82759,"time1":4,"time2":31},{"wh":117986,"dtype":4,"dist":996,"qty":1960,"priority":66889,"time1":3,"time2":35},{"wh":120762,"dtype":4,"dist":101,"qty":3610,"priority":89859,"time1":6,"time2":26},{"wh":208277,"dtype":4,"dist":1512,"qty":14,"priority":53599,"time1":4,"time2":49},{"wh":206348,"dtype":4,"dist":209,"qty":359,"priority":89859,"time1":5,"time2":27},{"wh":117501,"dtype":4,"dist":106,"qty":782,"priority":92959,"time1":1,"time2":26},{"wh":130744,"dtype":4,"dist":1421,"qty":94,"priority":53599,"time1":3,"time2":53}],"time1":1,"time2":26,"wh":117501,"dtype":4,"dist":106,"sign":"AAAAAAAAAAAAAAAAAAAAAAAAAAA=","payload":"y4MtaONO4gwJjIoUGedtEV+V0W1e+q8mkrkrrRddD6UwZ5TVJ5AA"}],"totalQuantity":6904,"time1":1,"time2":26,"wh":117501,"dtype":4,"dist":106}]}}
```
2. Далее я реализовал запрос к api и получение json-ответа:
```py
try:
    response = requests.get(
        api_url,
        headers=settings.HEADERS,  # header, который помогает замаскировать запрос под браузерный, будто бы он выполнен пользователем
        timeout=settings.TIMEOUT   # Защита от зависания процесса парсинга (максимальное время ожидания ответа от сервера в секундах)
    )
    response.raise_for_status()    # Проверка на 200
    return response.json()         # Возврат ответа api в json
except requests.RequestException:
    return None                    # Если возникла ошибка запроса возвращаем None
```
3. Извлек нужные параметры из ответа api, привёл их к нужному формату и вернул:
```py
products = api_data.get("data", {}).get("products", [])

if not products:
    return None                              # Если не нашлось товаров возвращаем None

product = products[0]                        # Берём первый элемент из списка (наш товар)
price = int(product.get("priceU", 0)) / 100  # Приводим цену к рублям (в ответе сервера цена указывается в копейках)

product_data = {
    "product_name": product.get("name"),     # Получаем имя товара
    "product_price": f"{price:.2f} ₽",       # Цену товара указываем с точностью до 2 знаков
}

return product_data                          # Возвращаем словарь с данными о товаре
```
Таким образом на выходе мы получаем dict с именем и ценой товара.
Осталось только реализовать главную функцию, которая будет вызываться извне модуля:
```py
def get_wb_info(article: str) -> Optional[dict]:
    """ Получает информацию о товаре с Wildberries по его артикулу """
    api_data = fetch_api_data(article)
    if not api_data:
        return None

    return extract_product_data(api_data)
```

# Юзер-Мануал:
### Установка:
1. Склонировать репозиторий и перейти в него
```console
git clone https://github.com/linkoffee/wb-parser.git
```
```console
cd wb-parser/
```
2. Создать виртуальное окружение `(python 3.11)` и активировать
```console
py -3.11 -m venv venv
```
```console
source venv/bin/activate      # Linux/MacOS
source venv\Scripts\activate  # Windows
```
3. Установить зависимости
```console
pip install -r requirements.txt
```
### Использование:
1. Находясь в корневой директории введите в консоли:
```console
py main.py
```
2. Введите артикул товара с WB:
```console
$ py main.py 
Enter WB product article: <article>
```
### Структура проекта:
```
wb-parser/            # root
├── modules/          # Пакет с модулями
│   ├── __init__.py   
│   ├── settings.py   # Настройки парсера
│   └── wb_parse.py   # Модуль WB-парсера
├── .gitignore
├── main.py           # Точка входа
└── requirements.txt  # Файл с зависимостями
```
Проект построен таким образом, чтобы его можно было расширять в случае необходимости.

---

Автор: [Mikhail Kopochinskiy](https://github.com/linkoffee)
