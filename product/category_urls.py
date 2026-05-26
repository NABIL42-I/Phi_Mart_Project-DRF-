from django.urls import path
from . import views

# urlpatterns = [
#     # path('',views.view_categories,name="category_list"),
#     path('',views.ViewCategories.as_view(),name="category_list"),
#     # path('<int:pk>/',views.view_specific_categories,name="view_specific_category"),
#     # path('<int:pk>/',views.ViewSpecificCategories.as_view(),name="view_specific_category"),
#     path('<int:pk>/',views.CategoryDetails.as_view(),name="view_specific_category"),

# ]