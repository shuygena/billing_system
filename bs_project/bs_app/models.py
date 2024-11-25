from django.db import models

CURRENCY_CHOICES = [("RUB", "RUB"), ("USD", "USD")]

TRANSACTION_STATUS_CHOICES = [
    ("NEW", "NEW"),
    ("Completed", "Completed"),
    ("Rejected", "Rejected"),
]


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, null=False, blank=False
    )
    currency_balance = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="RUB", null=False, blank=False
    )

    def __str__(self):
        return f"{self.customer_id} {self.name}"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    currency_price = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="RUB", null=False, blank=False
    )
    available_quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.product_id} {self.name}"


class Transaction(models.Model):
    # TODO: Create class Payment(Transaction)
    transaction_id = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=10, choices=TRANSACTION_STATUS_CHOICES, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False, blank=False
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )
    product_quantity = models.PositiveIntegerField(null=False)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="RUB", null=False
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
