from django.urls import path
from .views import (
    CustomerRegistration,
    CustomerDetail,
    ProductCreation,
    PaymentCreation,
    TransactionDetail,
    TransactionsCustomersMapping,
    TransactionsAmountMapping,
    CustomersCompaniesMapping,
    ProductsPriceMapping,
)


urlpatterns = [
    path("customer/", CustomerRegistration.as_view(), name="Customer-register"),
    path(
        "customer/id=<int:customer_id>/",
        CustomerDetail.as_view(),
        name="Customer-detail",
    ),
    path("product/", ProductCreation.as_view(), name="Product-create"),
    path("payment/", PaymentCreation.as_view(), name="Payment-create"),
    path(
        "transaction/id=<int:transaction_id>/",
        TransactionDetail.as_view(),
        name="Transaction-detail",
    ),
    path(
        "transaction/customer_id=<int:customer_id>/",
        TransactionsCustomersMapping.as_view(),
        name="Transaction-customer",
    ),
    path(
        "transaction/amount_range=<int:amount_range>/currency=<str:currency>/",
        TransactionsAmountMapping.as_view(),
        name="Transaction-amount",
    ),
    path(
        "customer/company=<str:company>/",
        CustomersCompaniesMapping.as_view(),
        name="Customer-company",
    ),
    path(
        "product/price_range=<str:price_range>/currency=<str:currency>/",
        ProductsPriceMapping.as_view(),
        name="Product-price",
    ),
]
