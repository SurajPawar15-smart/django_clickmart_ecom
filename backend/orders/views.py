from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, CartItem
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework import status
from .utils import send_order_notification
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.db import transaction

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or cart.items.count() == 0:
            return Response({"error": "Cart is empty"}, status=400)

        shipping_address = request.data.get("shippingAddress") or {}
        address = shipping_address.get("address", "Default Address")
        phone = shipping_address.get("phone", "0000000000")
        city = shipping_address.get("city", "Default City")
        state = shipping_address.get("state", "Default State")
        zip_code = shipping_address.get("zipCode", "000000")

        with transaction.atomic():
            # Check stock
            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    return Response(
                        {"details": f'Only {item.product.stock} left for {item.product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create order
            order = Order.objects.create(
                user=request.user,
                subtotal=cart.subtotal,
                tax_amount=cart.tax_amount,
                grand_total=cart.grand_total,
                address=address,
                phone=phone,
                city=city,
                state=state,
                zip_code=zip_code,
            )

            # Deduct stock and create order items
            for item in cart.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price,
                    total_price=item.total_price
                )

            # Clear cart
            cart.items.all().delete()

            # Send notification email
            send_order_notification(order)

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk, user=self.request.user)
        return order