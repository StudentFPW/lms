from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as NativeGroup

from .models import Product, Lesson, Group, GroupMembership
from .serializers import (
    ProductWithStatsSerializer,
    LessonSerializer,
    GroupSerializer,
    GroupMembershipSerializer,
)


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductWithStatsSerializer


class LessonAPIView(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListByProduct(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        product = Product.objects.get(id=product_id)

        user = User.objects.get(username=self.request.user)
        group = NativeGroup.objects.get(name=product.name.lower().replace(" ", "_"))

        if group in user.groups.all():
            return Lesson.objects.filter(product=product_id)
        return Lesson.objects.none()


class GroupAPIView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupMembershipAPIView(ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
