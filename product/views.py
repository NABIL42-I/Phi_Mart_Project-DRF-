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
    queryset = Product.objects.all()
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


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    def perform_create(self,serializer):
        # serializer.save(product_id = self.kwargs['product_pk'])# give error in Swagger
        serializer.save(product_id = self.kwargs.get('product_pk'))

   


# CategoryList + CategoryDEtails
class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        product_count=Count('products')).all()
    serializer_class = CategorySerializer


#Generic Api View
class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class  = CategorySerializer




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






# #Viewset use Router
# # (ViewProduct+ProductDetails)
# class productViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
#     # filterset_fields = ['category_id','price']
#     filterset_class = ProductFilter
#     pagination_class = DefaultPagination
#     search_fields = ['name','description','category__name']
#     ordering_fields = ['price','updated_at']
#     permission_classes=[IsAdminOrReadOnly]
#     # permission_classes = [DjangoModelPermissions]
#     # permission_classes = [FullDjangoModelPermission]#Roled-Based-Control
#     # def get_permissions(self): #is an instance method
#     #     if self.request.method == 'GET':
#     #         # return [AllowAny]#return class (wrong)
#     #         return [AllowAny()] #return class obj
#     #     return [IsAdminUser()]

#     # def get_queryset(self):
#     #     queryset = Product.objects.all()
#     #     category_id = self.request.query_params.get('category_id')
#     #     if category_id is not None:
#     #         queryset = Product.objects.filter(category_id=category_id)
#     #     return queryset
       
#     #override from  mixins.DestroyModelMixin class
#     # def destroy(self,request,*args,**kwargs):
#     #     product = self.get_object()
#     #     if product.stock>10:
#     #         return Response({'message':'Product with stock more than 10 could not be deleted'})
#     #     self.perform_destroy(product)
#     #     return Response( status=status.HTTP_204_NO_CONTENT)   










# @api_view(['GET','POST'])
# def view_products(request):
#     if request.method=='GET':
#         # products = Product.objects.all()
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products,many = True, context={'request': request})
#         return Response(serializer.data)
#     if request.method == 'POST':
#         # Deserializer
#         serializer = ProductSerializer(
#             data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     # else:
#         #  return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


# class ViewProduct(APIView):
#     def get(self,request):
#         # products = Product.objects.all()
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products,many = True, context={'request': request})
#         return Response(serializer.data)
#     def post(self,request):#create Product
#         # Deserializer
#         serializer = ProductSerializer(
#             data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class ProductList(ListCreateAPIView):
#     # queryset = Product.objects.select_related('category').all()
#     # serializer_class = ProductSerializer
#     def get_queryset(self):
#         return Product.objects.select_related('category').all()
#     def get_serializer_class(self):
#         return ProductSerializer
#     # def get_serializer_class(self):
#     #     return {'request':self.request}

# @api_view(['GET', 'PUT', 'DELETE'])
# def view_specific_product(request, id):
#     if request.method == 'GET':
#         # use get_object_or_404 instead of try except
#         # product = get_object_or_404(Product, pk=id)
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     if request.method == 'PUT': #Update existing Product
#         # product = get_object_or_404(Product, pk=id)
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     if request.method == 'DELETE':
#         product = get_object_or_404(Product, pk=id)
#         copy_of_product = product
#         product.delete()
#         serializer = ProductSerializer(copy_of_product)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     #generic view by default search query by pk not id
#     queryset = Product.objects.all()
#     serializer_class=ProductSerializer
#     lookup_field = 'id'
#     # override the delete method
#     def delete(self,request,id):
#         product = get_object_or_404(Product, pk=id)
#         if product.stock>10:
#             return Response({'message':'Product with stock more than 10 could not be deleted'})
#         product.delete()
#         return Response( status=status.HTTP_204_NO_CONTENT)   



# class ViewSpecificProduct(APIView):
#     def get(self,request,id):
#         # use get_object_or_404 instead of try except
#         # product = get_object_or_404(Product, pk=id)
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self,request,id):#Update Existing Product
#         # product = get_object_or_404(Product, pk=id)
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,id):
#         product = get_object_or_404(Product, pk=id)
#         copy_of_product = product
#         product.delete()
#         serializer = ProductSerializer(copy_of_product)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)   


    # try:
    #     product = Product.objects.get(pk=id)
    #     product_dict = {'id':product.id,'name':product.name,'price':product.price}
    #     return Response(product_dict)
    # except Product.DoesNotExist:
    #     return Response({'message':"Product does not exists"},status=status.HTTP_404_NOT_FOUND)



# @api_view()
# def view_categories(request):
#     categories = Category.objects.annotate(
#     product_count=Count('products')).all()
#     serializer = CategorySerializer(categories,many = True)
#     return Response(serializer.data)
# class ViewCategories(APIView):
#     def get(self,request):
#         categories = Category.objects.annotate(
#         product_count=Count('products')).all()
#         serializer = CategorySerializer(categories,many = True)
#         return Response(serializer.data)
#     def post(self,request):#Create
#         #it convert json to object for save in database
#         serializers = CategorySerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)





# @api_view()
# def view_specific_categories(request,pk):
#     #use get_object_or_404 instead of try except
#         category = get_object_or_404(Category,pk=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)


# class ViewSpecificCategories(APIView):
#     def get(self,request,pk):
#         category = get_object_or_404(
#         #add a new col name product_count
#         Category.objects.annotate(
#         product_count=Count('products')).all(),pk = pk
#         )
#         serializers = CategorySerializer(category)
#         return Response(serializers.data)
#     def put(self,request,pk):   
#         category = get_object_or_404(
#         #add a new col name product_count
#         Category.objects.annotate(
#         product_count=Count('products')).all(),pk = pk
#         ) 
#         serializer = CategorySerializer(category,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,reqeust,pk):
#         category = get_object_or_404(
#         #add a new col name product_count
#         Category.objects.annotate(
#         product_count=Count('products')).all(),pk = pk
#         )  
#         copy_of_product = category      
#         category.delete()
#         serializer = CategorySerializer(copy_of_product)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)      


