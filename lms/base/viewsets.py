from rest_framework import generics
from .models import Product, Lesson
from .serializers import ProductSerializer, LessonSerializer, ProductDetailSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListWithDetailsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs["product_id"]
        # Получаем список уроков по конкретному продукту, к которому пользователь имеет доступ
        return Lesson.objects.filter(
            product_id=product_id, product__product_access__user=user
        )
