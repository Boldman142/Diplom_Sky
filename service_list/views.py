from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from service_list.models import Category, Product

from django.urls import reverse_lazy, reverse
from service_list.forms import ProductForm
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Методы обследований:'
    }


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('service_list:category_list')

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
        return reverse('service_list:product_detail', args=[self.get_object().pk])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_staff:
            raise Http404
        return self.object


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        return Product.objects.filter(category_id=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        prod_type = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Обследования из раздела: {prod_type.name}'
        return context_data


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('service_list:category_list')
