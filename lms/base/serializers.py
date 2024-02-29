from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product, Lesson, Group, GroupMembership


class ProductWithStatsSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "start_date",
            "cost",
            "num_students",
            "num_lessons",
            "group_fill_percentage",
            "purchase_percentage",
        ]

    def get_num_lessons(self, obj):
        return Lesson.objects.filter(product=obj).count()

    def get_num_students(self, obj):
        return GroupMembership.objects.filter(group__product=obj).count()

    def get_group_fill_percentage(self, obj):
        total_fill_percentage = 0
        groups = obj.group_set.all()
        count_user = GroupMembership.objects.filter(group__product=obj).count()
        for group in groups:
            if group.max_users != 0:
                fill_percentage = count_user / group.max_users * 100
                total_fill_percentage += fill_percentage
        if groups.count() != 0:
            return total_fill_percentage / groups.count()
        return 0

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        count_user = GroupMembership.objects.filter(group__product=obj).count()
        if total_users != 0:
            accesses = count_user
            return accesses / total_users * 100
        return 0


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "product", "name", "video_link")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "product", "name", "min_users", "max_users")


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ("id", "group", "user")
