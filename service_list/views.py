from django.shortcuts import render

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from service_list.models import Category


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Методы обследований:'
    }
