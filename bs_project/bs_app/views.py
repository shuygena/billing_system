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
)


class CustomerRegistration(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return JsonResponse(
                {"status": "Customer created", "customer_id": customer.customer_id},
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomerSerializer(customer)
        return JsonResponse(serializer.data)


class ProductCreation(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return JsonResponse(
                {"status": "Product created", "product_id": product.product_id},
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCreation(APIView):
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


class TransactionDetail(APIView):
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return JsonResponse(
                {"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)


class TransactionsCustomersMapping(APIView):
    # TODO: check existing customer_id, if it doesn't exist - return error
    def get(self, request, customer_id):
        ts = get_transactions_by_customer_id(customer_id)
        return JsonResponse(ts, safe=False)


class TransactionsAmountMapping(APIView):
    def get(self, request, amount_range, currency):
        if currency not in ("RUB", "USD"):
            return JsonResponse(
                {"error": "Not valid currency"}, status=status.HTTP_400_BAD_REQUEST
            )
        ts = get_transactions_by_amount_range(amount_range, currency)
        return JsonResponse(ts, safe=False)


class CustomersCompaniesMapping(APIView):
    # TODO: check existing company, if it doesn't exist - return error
    def get(self, request, company):
        cs = get_customers_by_company(company)
        return JsonResponse(cs, safe=False)


class ProductsPriceMapping(APIView):
    def get(self, request, price_range, currency):
        if currency not in ("RUB", "USD"):
            return JsonResponse(
                {"error": "Not valid currency"}, status=status.HTTP_400_BAD_REQUEST
            )
        ps = get_product_by_price_range(price_range, currency)
        return JsonResponse(ps, safe=False)
