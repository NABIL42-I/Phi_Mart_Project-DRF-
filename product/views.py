from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product,Category,Review,ProductImage
from rest_framework import status
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
# from rest_framework.pagination import PageNumberPagination
from product.paginations import DefaultPagination
# from rest_framework.permissions import IsAdminUser,AllowAny
from api.permissions import IsAdminOrReadOnly,FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


#Viewset use Router
# (ViewProduct+ProductDetails)
class productViewSet(ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['category_id','price']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name','description','category__name']
    ordering_fields = ['price','updated_at']
    permission_classes=[IsAdminOrReadOnly]
    @swagger_auto_schema(
        operation_summary='Retrive a list of products'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow an admin to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()



class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    def perform_create(self,serializer):
        # serializer.save(product_id = self.kwargs['product_pk'])# give error in Swagger
        serializer.save(product_id = self.kwargs.get('product_pk'))

   


# CategoryList + CategoryDEtails
# class CategoryViewSet(ModelViewSet):
#     permission_classes=[IsAdminOrReadOnly]
#     queryset = Category.objects.annotate(
#         product_count=Count('products')).all()
#     serializer_class = CategorySerializer

class CategoryViewSet(ModelViewSet):
    """
    list:
    Retrieve a list of categories along with their product counts and nested product data.
    
    retrieve:
    Get details of a single category, including all related items.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(
        product_count=Count('products')
    ).prefetch_related(
        'products__images'  # <-- This pulls all product images in 1 query, stopping the 49 extra calls
    ).all()

#Generic Api View
# class CategoryDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.annotate(product_count=Count('products')).all()
#     serializer_class  = CategorySerializer




class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadonly]
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}





