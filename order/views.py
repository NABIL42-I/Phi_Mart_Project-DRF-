from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer
    #Allowed Method [must be in lowercase]
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method =='POST':
            return AddCartItemSerializer
        if self.request.method =='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])


class Orderviewset(ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    