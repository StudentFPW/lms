from rest_framework import serializers
from .models import Product, Lesson, Group


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "creator", "name", "start_date", "cost")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "product", "name", "video_link")


class ProductDetailSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "creator",
            "name",
            "start_date",
            "cost",
            "num_students",
            "group_fill_percentage",
            "purchase_percentage",
        )

    def get_num_students(self, obj):
        # Получаем количество учеников занимающихся на продукте
        return ProductAccess.objects.filter(product=obj).count()

    def get_group_fill_percentage(self, obj):
        # Рассчитываем процент заполненности группы для каждого продукта
        groups = Group.objects.filter(product=obj)
        total_percentage = 0
        total_groups = 0
        for group in groups:
            fill_percentage = (
                group.groupmembership_set.count() / group.max_users
            ) * 100
            total_percentage += fill_percentage
            total_groups += 1
        if total_groups == 0:
            return 0
        else:
            return total_percentage / total_groups

    def get_purchase_percentage(self, obj):
        # Рассчитываем процент приобретения продукта
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        else:
            return (
                ProductAccess.objects.filter(product=obj).count() / total_users
            ) * 100
