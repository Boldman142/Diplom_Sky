from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from service_list.models import Category, Product
from users.models import User


class ProductTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test5@test.ru',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.category = Category.objects.create(
            name='Testovoe',
            overview='Test21'
        )
        self.product = Product.objects.create(
            name='Testovoe1',
            overview='Test',
            overview_big='Test big',
            creator=self.user,
            category=self.category,
            price=2000
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_list_category(self):
        """Тестирование просмотра списка обследований в категории"""
        response = (self.client.get(
            reverse('service_list:category', args=[self.category.id])
        ))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_product(self):
        """Тестирование просмотра обследования"""
        response = self.client.get(
            reverse('service_list:product_detail', args=[self.product.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_product(self):
        """Тестирование изменения обследования"""
        data = {
            "name": "Testovoe22",
            "overview": "Opyat Testovoe"
        }

        response = self.client.put(
            reverse('service_list:product_update',
                    args=[self.product.id]), data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )

    def test_delete_product(self):
        """Тестирование удаления обследования"""
        response = self.client.delete(
            reverse('service_list:product_delete', args=[self.product.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )


class CreateProductTestCase(APITestCase):
    url = reverse('service_list:product_create')

    def setUp(self):
        self.active_user = User.objects.create(
            email='test@example.com', is_active=True
        )
        self.category = Category.objects.create(
            name='Testovoe', overview='Test21'
        )

    def test_anonymous_user_cannot_create_product(self):
        """Тест невозможности создания обследования анонимному пользователю"""
        data = self._get_create_product_data()

        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Product.objects.exists())

    def test_created_product_belongs_current_user(self):
        """Тест возможности создания обследования авторизованному пользователю"""
        self.client.force_login(user=self.active_user)
        data = self._get_create_product_data()

        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = Product.objects.get()
        self.assertEqual(product.creator, self.active_user)

    def test_failed_to_create_product_with_negative_price(self):
        """Тест невозможности создания обследования с отрицательной ценой"""
        self.client.force_login(user=self.active_user)
        data = self._get_create_product_data(price=-100)
        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = Product.objects.get()
        self.assertEqual(product.creator, self.active_user)

    def _get_create_product_data(self, **override):
        """Тест создания обследования с правильным наполнением"""
        data = {
            'name': 'Some Name',
            'overview': 'Overview',
            'price': 10_000,
            'overview_big': 'Overview Big',
            'category': self.category.id
        }
        return data | override
