from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from carts.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .utils import send_order_notification

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer

# Create your views here.
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)

        items = cart.items.select_related('product')

        if not items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # calculate totals safely
        subtotal = sum(item.quantity * item.product.price for item in items)
        tax_amount = sum(
            item.quantity * item.product.price * (item.product.tax_percent / 100)
            for item in items
        )
        grand_total = subtotal + tax_amount

        # create order
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            tax_amount=tax_amount,
            grand_total=grand_total
        )

        # create order items + reduce stock
        for item in items:
            product = item.product

            if item.quantity > product.stock:
                raise ValueError(f"Not enough stock for {product.name}")

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )

            product.stock -= item.quantity
            product.save()

        # clear cart
        items.delete()

        # send email notification
        send_order_notification(order)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items__product')
            .order_by('-created_at')
        )
