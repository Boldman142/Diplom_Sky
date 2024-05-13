from django.shortcuts import render

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from service_list.models import Category, Product

from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from service_list.forms import ProductForm
# from catalog.models import Category, Product, Version
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django import forms



# from core import settings




class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Методы обследований:'
    }

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    form_class = ProductForm

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_update', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    permission_required = 'catalog.view_product'


class ProductListView(ListView):
    model = Product

    # def get_queryset(self, *args, **kwargs):
    #     category = self.kwargs.get('pk')
    #     return get_prod_categories_cache(category)

    def get_context_data(self, *args, **kwargs):
        prod_type = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Обследования типа: {prod_type.name}'

        # products = context_data['object_list']
        #
        # for product in products:
        #     product.is_active_vers = product.version_set.filter(sign=True)

        return context_data


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('service_list:catalog')
