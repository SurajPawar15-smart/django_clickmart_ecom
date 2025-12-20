from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    tax_percent = serializers.DecimalField(source='product.tax_percent', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_subtotal(self, obj):
        return sum(
            item.quantity * item.product.price
            for item in obj.items.all()
        )

    def get_grand_total(self, obj):
        subtotal = self.get_subtotal(obj)
        tax_total = sum(
            item.quantity * item.product.price * (item.product.tax_percent / 100)
            for item in obj.items.all()
        )
        return subtotal + tax_total
