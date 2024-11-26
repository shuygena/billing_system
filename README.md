# Система биллинга

## :toolbox: Зависимости 
Есть два способа запуска проекта:
1. Используя docker compose. Требуются docker, docker compose, etc.
2. Без него: python-3.8.10, postgersql, etc.
Также в проекте есть скрипт для выполнения запросов, для которого требуется python.

## :octopus:  Запуск с помощью docker compose

1. Склонируйте репозиторий `git clone https://github.com/shuygena/billing_system`  
2. Перейдите в папку с проектом `cd billing_system`  
3. Выполните команду `docker compose build`  
4. Выполните команду `docker compose up`  
5. Запросы выполняйте к адресу `http://localhost:8000`. К серверу можно обратиться через веб-интерфейс.

Может возникнуть проблема с портами `- "5432:5432"`, они могут быть заняты. Можно освободить порты, либо изменить их в `docker-compose.yml`.

## :computer: Локальный запуск
Ожидается, что существует пользователь postgresql с именем `ordinary_user` и паролем `pass1234`, а также база данных `bs_db`.  
Шаги по созданию:
```
sudo -u postgres psql
CREATE USER ordinary_user WITH PASSWORD pass1234;
CREATE DATABASE bs_db;
GRANT ALL PRIVILEGES ON DATABASE bs_db to ordinary_user;
```
Или же можно прописать свои настройки в `bs_project/bs_project/bs_project/settings.py` (DATABASE).
> TODO: добавить .env

1. Склонируйте репозиторий `git clone https://github.com/shuygena/billing_system`  
2. Перейдите в папку с проектом `cd bs_project`
3. Создайте виртуальное окружение `python3 -m venv .venv`
4. Активируйте виртуальное оружение `source .venv/bin/activate`
5. Установите зависимости `pip install -r requirements.txt`
6. Перейдите в директорию `cd bs_project`
7. Создайте миграции `python3 manage.py makemigrations`
8. Запустите миграции `python3 manage.py makemigrate`
9. Запустите сервер `python3 manage.py runserver`
10. Запросы выполняйте к адресу `http://localhost:8000`. К серверу можно обратиться через веб-интерфейс.

### POST
![image](https://github.com/user-attachments/assets/b816ee51-9ef8-45b9-ae5d-431b5df8f2f2)
POST-запросы:
```
/customer/
/product/
/payment/
```
Пример customer:
```
{
    "name": "Stuart", # имя 
    "company": "Minion",  # компания
    "balance": 100,  # баланс
    "currency_balance": "RUB"  # валюта баланса
    }
```
Пример product:  
```
{
    "name": "tea with my tears",  # название продукта
    "price": 13.5,  #  стоимость продукта
    "currency_price": "USD", # валюта USD/RUB
    "available_quantity": 20, # доступное количество
}
```
Пример payment
```
{
    "customer": 1,  #  customer_id
    "product": 1,  #  product_id
    "product_quantity": 1,  #  желаемое количество продукта
}
```
### GET
Запрос с параметром `/customer/?id=1`  
![image](https://github.com/user-attachments/assets/d04d6425-15d0-434d-bcbb-119f798b8c4c)  
URL с параметром `/customer/id=1/`  
![image](https://github.com/user-attachments/assets/ed9b212d-42a4-4672-900d-0c4b98f11df2)  

Примеры GET-запросов c query-параметрами: 
```
/customer/?id=1  #  получить информацио о пользователе
/customer/?company=Minion  #  получить пользователей из одной компании
/transaction/?id=1   #  получить информацио о транзакции
/transaction/?customer_id=1  #  получить все транзакции пользователя
/transaction/?amount_range=100&currency=RUB  #  получить все транзакци в диапозоне суммы
/product/?price_range=15&currency=USD   #  получить все продукты в диапозоне цены
```
Примеры GET-запросов c url-параметрами: 
```
/customer/id=1  #  получить информацио о пользователе
/customer/company=Minion  #  получить пользователей из одной компании
/transaction/id=1   #  получить информацио о транзакции
/transaction/customer_id=1  #  получить все транзакции пользователя
/transaction/amount_range=100/currency=RUB/  #  получить все транзакци в диапозоне суммы
/product/price_range=15/currency=USD/   #  получить все продукты в диапозоне цены
```
запрос с фильтром:  
![image](https://github.com/user-attachments/assets/b3e3f808-8de5-4a15-8daa-661df84b5c1a)  

### Скрипт api_scenario.py
Посмотреть пример запросов к сиситеме можно запустив скрипт `api_scenario.py`. Для этого нужен установленный python и pip.
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requests
python3 api_scenario.py
```
Скрипт должен создать пользователей, продукты и транзакции, а затем сделать get-запросы. Осторожно, скрипт выдаёт очень много логов. Должен работать вне зависимосте от того как имено запускался сервер. 
Созданные пользователи (баланс после выполненных транзакций):
```
bs_db=# SELECT * FROM bs_app_customer;
 customer_id |   name    |  company  |  balance  | currency_balance
-------------+-----------+-----------+-----------+------------------
           2 | Kevin     | Minion    |    100.00 | USD
           4 | Alex Z.   | RKN       | 100000.00 | RUB
           1 | Bruce Lee | Freelance |  99986.50 | USD
           3 | Stuart    | Minion    |     60.00 | RUB
```
Продукты (количество после проведённых платежей):
```
bs_db=# SELECT * FROM bs_app_product;
 product_id |       name        | price | currency_price | available_quantity
------------+-------------------+-------+----------------+--------------------
          1 | tea with sugar    |  1.00 | USD            |                100
          2 | tea with my tears | 13.50 | USD            |                 19
          3 | banana            | 20.00 | RUB            |                998
```
Транзакции:
```
bs_db=# SELECT * FROM bs_app_transaction;
 transaction_id |  status   |          created_at           | product_quantity | currency | amount | customer_id | product_id
----------------+-----------+-------------------------------+------------------+----------+--------+-------------+------------
              1 | Completed | 2024-11-26 19:58:40.850007+03 |                1 | USD      |  13.50 |           1 |          2
              2 | Completed | 2024-11-26 19:58:40.990747+03 |                2 | RUB      |  40.00 |           3 |          3
              3 | Rejected  | 2024-11-26 19:58:41.140071+03 |                2 | RUB      |  40.00 |           2 |          3
              4 | Rejected  | 2024-11-26 19:58:41.278203+03 |                2 | USD      |   2.00 |           3 |          1
```

> Есть большая вероятность, что что-то пойдёт не по плану! Но у меня всё работает.
> TODO: Добавить тесты
