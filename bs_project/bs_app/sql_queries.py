from django.db import connection


def get_transactions_by_customer_id(customer_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM bs_app_transaction WHERE customer_id = %s;", [customer_id]
        )
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        transaction_list = [dict(zip(columns, row)) for row in rows]
    return transaction_list


def get_transactions_by_amount_range(amount_range, currency):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM bs_app_transaction WHERE amount <= %s AND currency LIKE %s;",
            [amount_range, currency],
        )
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        transaction_list = [dict(zip(columns, row)) for row in rows]
    return transaction_list


def get_customers_by_company(company):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM bs_app_customer WHERE company = %s;", [company])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        customers_list = [dict(zip(columns, row)) for row in rows]
    return customers_list


def get_product_by_price_range(price_range, currency):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM bs_app_product WHERE price <= %s AND currency_price LIKE %s;",
            [price_range, currency],
        )
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        product_list = [dict(zip(columns, row)) for row in rows]
    return product_list
