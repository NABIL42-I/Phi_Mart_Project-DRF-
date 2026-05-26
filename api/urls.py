from django.urls import path,include
# from rest_framework.routers import SimpleRouter,DefaultRouter
from product.views import productViewSet,CategoryViewSet,ReviewViewset
from rest_framework_nested import routers
from order.views import CartViewSet,CartItemViewSet,Orderviewset

# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products',productViewSet,basename='products')
router.register('categories',CategoryViewSet)
router.register('carts',CartViewSet, basename = 'carts')
router.register('orders',Orderviewset, basename = 'orders')

product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews',ReviewViewset, basename='Product-Review')# basename -> label name

# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

cart_router = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart_item')


# urlpatterns = router.urls

urlpatterns=[
    path('',include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    #aro urls thake segula ekhane dewa jabe 
    # path(r'', include(router.urls)),#Raw string

]


# urlpatterns = [
#     path('products/',include("product.product_urls")),
#     path('categories/',include("product.category_urls")),
# ]
