from rest_framework import serializers
from .models import Customer, Transaction, Product


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["customer_id", "name", "company", "balance", "currency_balance"]

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "name", "price", "currency_price", "available_quantity"]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    product_quantity = serializers.IntegerField(min_value=1)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Transaction
        fields = ["product", "product_quantity", "customer"]

    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["product_quantity"]
        customer = validated_data["customer"]
        amount = product.price * quantity
        currency = product.currency_price
        transaction = Transaction.objects.create(
            status="NEW",
            customer=customer,
            amount=amount,
            currency=currency,
            product=product,
            product_quantity=quantity,
        )
        return transaction

    def update(self, instance, validated_data):
        product = validated_data["product"]
        customer = validated_data["customer"]
        quantity = validated_data["product_quantity"]
        if (
            product.currency_price == customer.currency_balance
            and instance.amount <= customer.balance
            and product.available_quantity >= quantity
        ):
            product_instance = Product.objects.get(product_id=product.product_id)
            customer_instance = Customer.objects.get(customer_id=customer.customer_id)
            customer_instance.balance -= instance.amount
            product_instance.available_quantity -= quantity
            instance.status = "Completed"
            customer_instance.save()
            product_instance.save()
        else:
            instance.status = "Rejected"

        instance.save()
        return instance
