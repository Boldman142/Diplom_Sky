from django.urls import path

from service_list.apps import ServiceListConfig
from service_list.views import CategoryListView

app_name = ServiceListConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),

]
