from django.urls import path, include
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()
router.register(r"product", ProductAPIView)
router.register(r"lesson", LessonAPIView)
router.register(r"group", GroupAPIView)
router.register(r"group-members", GroupMembershipAPIView)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "product/<int:product_id>/lessons/",
        LessonListByProduct.as_view(),
        name="product-lessons",
    ),
]
