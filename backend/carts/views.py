from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from rest_framework.response import Response
from .serializers import CartSerializer,CartItemSerializer
from products.models import Product
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # get or create the cart for logged in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # ✅ default value

        if not product_id:
            return Response({'error': 'product_id is required'}, status=400)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'quantity must be a number'}, status=400)

        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}  # ✅ important
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):

        change = request.data.get('change')

        if change is None:
            return Response(
                {"error": "Provide 'change' field"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            change = int(change)
        except ValueError:
            return Response(
                {"error": "'change' must be an integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if change not in (-1, 1):
            return Response(
                {"error": "'change' must be +1 or -1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = get_object_or_404(
            CartItem,
            pk=item_id,
            cart__user=request.user
        )

        product = item.product

        # stock check when increasing
        if change > 0 and item.quantity + change > product.stock:
            return Response(
                {'error': 'Not enough stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_qty = item.quantity + change

        if new_qty <= 0:
            item.delete()
            return Response(
                {'success': 'Item removed'},
                status=status.HTTP_200_OK
            )

        item.quantity = new_qty
        item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = get_object_or_404(
            CartItem,
            pk=item_id,
            cart__user=request.user
        )
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
