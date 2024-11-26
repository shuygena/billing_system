from rest_framework import status

# from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Customer, Product, Transaction
from .serializers import CustomerSerializer, ProductSerializer, TransactionSerializer
from .sql_queries import (
    get_transactions_by_customer_id,
    get_transactions_by_amount_range,
    get_customers_by_company,
    get_product_by_price_range,
    get_transaction
)


def get_customer_detail(customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse(
            {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = CustomerSerializer(customer)
    return JsonResponse(serializer.data)


def get_customers_list(company):
    # TODO: check existing company, if it doesn't exist - return error
    customers = get_customers_by_company(company)
    return JsonResponse(customers, safe=False)


def get_products_list(price_range, currency):
    if currency not in ("RUB", "USD"):
        return JsonResponse(
            {"error": "Not valid currency"}, status=status.HTTP_400_BAD_REQUEST
        )
    ps = get_product_by_price_range(price_range, currency)
    return JsonResponse(ps, safe=False)


def get_transaction_info(transaction_id):
    transaction_row = get_transaction(transaction_id)
    return JsonResponse(transaction_row, safe=False)


def get_transactions_list_by_amount(amount_range, currency):
    if currency not in ("RUB", "USD"):
        return JsonResponse(
            {"error": "Not valid currency"}, status=status.HTTP_400_BAD_REQUEST
        )
    ts = get_transactions_by_amount_range(amount_range, currency)
    return JsonResponse(ts, safe=False)


def get_transactions_list_by_customer(customer_id):
    # TODO: check existing customer_id, if it doesn't exist - return error
    ts = get_transactions_by_customer_id(customer_id)
    return JsonResponse(ts, safe=False)


class CustomerProcess(APIView):
    def get(self, request):
        parameters_number = len(request.GET)
        if parameters_number == 0:
            super().http_method_not_allowed(request)
        customer_id = request.GET.get("id")
        company = request.GET.get("company")
        if customer_id and parameters_number == 1:
            if customer_id.isdigit():
                return get_customer_detail(customer_id)
        elif company and parameters_number == 1:
            return get_customers_list(company)
        return JsonResponse(
            {"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return JsonResponse(
                {"status": "Customer created", "customer_id": customer.customer_id},
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductProcess(APIView):
    def get(self, request):
        parameters_number = len(request.GET)
        if parameters_number == 0:
            super().http_method_not_allowed(request)
        price_range = request.GET.get("price_range")
        currency = request.GET.get("currency")
        if price_range and currency and parameters_number == 2:
            try:
                float(price_range)
                return get_products_list(price_range, currency)
            except ValueError:
                return JsonResponse({"error": "Can't count price"},
                                    status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "Bad request"},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return JsonResponse(
                {"status": "Product created", "product_id": product.product_id},
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Payment(APIView):
    def bank_simulate(self, transaction, data):
        transaction_instance = Transaction.objects.get(
            transaction_id=transaction.transaction_id
        )
        serializer = TransactionSerializer(data=data, instance=transaction_instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            self.bank_simulate(transaction, data=request.data)
            return JsonResponse(
                {
                    "status": "Payment created",
                    "transaction_id": transaction.transaction_id,
                },
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionProcess(APIView):
    def get(self, request):
        parameters_number = len(request.GET)
        transaction_id = request.GET.get("id")
        amount_range = request.GET.get("amount_range")
        currency = request.GET.get("currency")
        customer_id = request.GET.get("customer_id")
        if transaction_id and parameters_number == 1:
            if transaction_id.isdigit():
                return get_transaction_info(transaction_id)
        elif amount_range and currency and parameters_number == 2:
            try:
                float(amount_range)
                return get_transactions_list_by_amount(amount_range, currency)
            except ValueError:
                return JsonResponse({"error": "Bad request"},
                                    status=status.HTTP_400_BAD_REQUEST)
        elif customer_id and parameters_number == 1:
            if customer_id.isdigit():
                return get_transactions_list_by_customer(customer_id)
        return JsonResponse(
            {"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST
        )


class CustomerDetail(APIView):
    def get(self, request, customer_id):
        return get_customer_detail(customer_id)


class TransactionDetail(APIView):
    def get(self, request, transaction_id):
        return get_transaction_info(transaction_id)


class TransactionsCustomersMapping(APIView):
    def get(self, request, customer_id):
        return get_transactions_list_by_customer(customer_id)


class TransactionsAmountMapping(APIView):
    def get(self, request, amount_range, currency):
        return get_transactions_list_by_amount(amount_range, currency)


class CustomersCompaniesMapping(APIView):
    def get(self, request, company):
        return get_customers_list(company)


class ProductsPriceMapping(APIView):
    def get(self, request, price_range, currency):
        return get_products_list(price_range, currency)
