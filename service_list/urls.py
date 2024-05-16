from django.urls import path

from service_list.apps import ServiceListConfig
from service_list.views import (CategoryListView, ProductListView,
                                ProductDetailView, ProductCreateView,
                                ProductUpdateView, ProductDeleteView)

app_name = ServiceListConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', ProductListView.as_view(), name='category'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete')

]
