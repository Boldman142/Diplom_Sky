from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from service_list.models import Category, Product
from users.models import User


class LessonTestCase(APITestCase):

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

        self.client.force_login(
            user=self.user
        )

    def test_create_product(self):
        """Тестирование создание обследования"""
        data = model_to_dict(self.product, exclude=['picture'])
        response = self.client.post(
            '/service_list/product/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
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
            status.HTTP_200_OK
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
