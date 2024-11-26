import requests
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://127.0.0.1:8000"

PRODUCTS = [
    {
        "name": "tea with sugar",
        "price": 1,
        "currency_price": "USD",
        "available_quantity": 100,
    },
    {
        "name": "tea with my tears",
        "price": 13.5,
        "currency_price": "USD",
        "available_quantity": 20,
    },
    {
        "name": "banana",
        "price": 20,
        "currency_price": "RUB",
        "available_quantity": 1000,
    },
]

CUSTOMERS = [
    {
        "name": "Bruce Lee",
        "company": "Freelance",
        "balance": 100000,
        "currency_balance": "USD",
    },
    {
        "name": "Kevin",
        "company": "Minion",
        "balance": 100,
        "currency_balance": "USD"
        },
    {
        "name": "Stuart",
        "company": "Minion",
        "balance": 100,
        "currency_balance": "RUB"
        },
    {
        "name": "Alex Z.",
        "company": "RKN",
        "balance": 100000,
        "currency_balance": "RUB",
    },
]


def add_product(new_product):
    try:
        response = requests.post(f"{BASE_URL}/product/", json=new_product)
        log.info(response.text)
        return response.json().get("product_id")
    except Exception as e:
        log.warning("Failed request: %s", e)


def add_customer(new_customer):
    try:
        response = requests.post(f"{BASE_URL}/customer/", json=new_customer)
        log.info(response.text)
        return response.json().get("customer_id")
    except Exception as e:
        log.warning("Failed request: %s", e)


def add_payment(new_payment):
    try:
        response = requests.post(f"{BASE_URL}/payment/", json=new_payment)
        log.info(response.text)
        return response.json().get("transaction_id")
    except Exception as e:
        log.warning("Failed request: %s", e)


def get_new_transactons(customers, products):
    new_transactions = [
        {
            "customer": customers["Bruce Lee"],
            "product": products["tea with my tears"],
            "product_quantity": 1,
        },
        {
            "customer": customers["Stuart"],
            "product": products["banana"],
            "product_quantity": 2,
        },
        {
            "customer": customers["Kevin"],
            "product": products["banana"],
            "product_quantity": 2,
        },
        {
            "customer": customers["Stuart"],
            "product": products["tea with sugar"],
            "product_quantity": 2,
        },
    ]
    return new_transactions


def get_request(request_path):
    try:
        response = requests.get(request_path)
        if response.status_code == 200:
            log.info(f"request:{request_path}\n {response.text}")
    except Exception as e:
        log.warning("Failed request: %s", e)

def get_request_with_params(request_path, query_params):
    try:
        response = requests.get(request_path, params=query_params)
        if response.status_code == 200:
            log.info(f"request:{request_path}\n {response.text}")
    except Exception as e:
        log.warning("Failed request: %s", e)


def api_scenario():
    customers = {customer["name"]: add_customer(customer) for customer in CUSTOMERS}
    products = {product["name"]: add_product(product) for product in PRODUCTS}
    new_transactions = get_new_transactons(customers, products)
    transaction_ids = [add_payment(transaction) for transaction in new_transactions]
    p_list = [
        f"{BASE_URL}/customer/id={customers['Stuart']}",
        f"{BASE_URL}/customer/company=Minion",
        f"{BASE_URL}/transaction/id={transaction_ids[0]}",
        f"{BASE_URL}/transaction/customer_id={customers['Kevin']}",
        f"{BASE_URL}/transaction/amount_range=100/currency=RUB/",
        f"{BASE_URL}/product/price_range=15/currency=USD/",
    ]
    for path in p_list:
        get_request(path)

    get_request_with_params(f"{BASE_URL}/customer/",
                            {"id": 1})
    get_request_with_params(f"{BASE_URL}/customer/",
                            {"company": "Minion"})
    get_request_with_params(f"{BASE_URL}/transaction/",
                            {"id": 1})
    get_request_with_params(f"{BASE_URL}/transaction/",
                            {"customer_id": 1})
    get_request_with_params(f"{BASE_URL}/transaction/",
                            {"amount_range": 100, "currency": "RUB"})
    get_request_with_params(f"{BASE_URL}/product/",
                            {"price_range": 13.60, "currency": "USD"})

if __name__ == "__main__":
    api_scenario()
