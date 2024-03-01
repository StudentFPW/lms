from django.contrib.auth.models import User
from django.contrib.auth.models import Group as NativeGroup

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime

from .models import Product, Lesson, Group, GroupMembership
from .serializers import ProductWithStatsSerializer


class LessonListByProductTestCase(TestCase):
    """
    Этот тест создает несколько объектов модели (пользователь, продукт, группа и уроки),
    а затем проверяет различные сценарии получения списка уроков для продукта.
    Тест проверяет, что для аутентифицированного пользователя вход в группу разрешен
    и уроки возвращаются, а для неаутентифицированного пользователя возвращается код 403.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            creator=self.user,
            name="Test Product",
            start_date=datetime(2022, 3, 1, 10, 30),
            cost=1.0,
        )
        self.lesson1 = Lesson.objects.create(
            product=self.product,
            name="Test lesson 1",
            video_link="http://www.youtube.com/",
        )
        self.lesson2 = Lesson.objects.create(
            product=self.product,
            name="Test lesson 2",
            video_link="http://www.youtube.com/",
        )
        self.group = Group.objects.create(
            product=self.product, name="Test Group", min_users=1, max_users=10
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_queryset_authenticated_user_in_group(self):
        group = NativeGroup.objects.get(
            name=self.product.name.lower().replace(" ", "_")
        )
        self.user.groups.add(group)
        url = reverse("product-lessons", kwargs={"product_id": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_queryset_authenticated_user_not_in_group(self):
        url = reverse("product-lessons", kwargs={"product_id": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_queryset_unauthenticated_user(self):
        self.client.logout()
        url = reverse("product-lessons", kwargs={"product_id": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ProductWithStatsSerializerTestCase(TestCase):
    """
    В этом тесте мы создаем несколько объектов моделей (пользователи, продукт, группу,
    членство в группе и уроки) в методе setUp(). Затем мы сериализуем объект Product с
    помощью ProductWithStatsSerializer и проверяем, что полученные данные соответствуют
    ожидаемым значениям.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="12345")
        self.user2 = User.objects.create_user(username="testuser2", password="12345")
        self.user3 = User.objects.create_user(username="testuser3", password="12345")
        self.user4 = User.objects.create_user(username="testuser4", password="12345")
        self.user5 = User.objects.create_user(username="testuser5", password="12345")
        self.user6 = User.objects.create_user(username="testuser6", password="12345")
        self.user7 = User.objects.create_user(username="testuser7", password="12345")
        self.user8 = User.objects.create_user(username="testuser8", password="12345")
        self.user9 = User.objects.create_user(username="testuser9", password="12345")
        self.user10 = User.objects.create_user(username="testuser10", password="12345")

        self.product = Product.objects.create(
            creator=self.user1, name="Test Product", start_date=datetime.now(), cost=10
        )
        self.lesson1 = Lesson.objects.create(
            product=self.product,
            name="Test lesson 1",
            video_link="http://www.youtube.com/",
        )
        self.lesson2 = Lesson.objects.create(
            product=self.product,
            name="Test lesson 2",
            video_link="http://www.youtube.com/",
        )
        self.group = Group.objects.create(
            product=self.product, name="Test Group", min_users=1, max_users=10
        )

        self.group_membership1 = GroupMembership.objects.create(
            user=self.user1, group=self.group
        )
        self.group_membership2 = GroupMembership.objects.create(
            user=self.user2, group=self.group
        )
        self.group_membership3 = GroupMembership.objects.create(
            user=self.user3, group=self.group
        )
        self.group_membership4 = GroupMembership.objects.create(
            user=self.user4, group=self.group
        )
        self.group_membership5 = GroupMembership.objects.create(
            user=self.user5, group=self.group
        )
        self.group_membership6 = GroupMembership.objects.create(
            user=self.user6, group=self.group
        )
        self.group_membership7 = GroupMembership.objects.create(
            user=self.user7, group=self.group
        )
        self.group_membership8 = GroupMembership.objects.create(
            user=self.user8, group=self.group
        )
        self.group_membership9 = GroupMembership.objects.create(
            user=self.user9, group=self.group
        )
        self.group_membership10 = GroupMembership.objects.create(
            user=self.user10, group=self.group
        )

    def test_product_with_stats_serializer(self):
        serializer = ProductWithStatsSerializer(instance=self.product)
        expected_num_students = 10
        expected_num_lessons = 2
        expected_group_fill_percentage = 100.0
        expected_purchase_percentage = 100.0
        self.assertEqual(serializer.data["num_students"], expected_num_students)
        self.assertEqual(serializer.data["num_lessons"], expected_num_lessons)
        self.assertEqual(
            serializer.data["group_fill_percentage"], expected_group_fill_percentage
        )
        self.assertEqual(
            serializer.data["purchase_percentage"], expected_purchase_percentage
        )
