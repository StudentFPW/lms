from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth.models import Group as NativeGroup
from django.contrib.auth.models import Permission

from .models import Product, Group, GroupMembership


@receiver(post_save, sender=Product)
def create_product_group(sender, instance, created, **kwargs):
    if created:
        group_name = instance.name.lower().replace(" ", "_")
        group, created = NativeGroup.objects.get_or_create(name=group_name)

        permission = Permission.objects.get(codename="view_product")
        group.permissions.add(permission)
        group.save()


@receiver(pre_save, sender=Product)
def check_start_date(sender, instance, **kwargs):
    if instance.start_date < timezone.now():
        raise ValidationError("Дата начала не может быть в прошлом!")
    if instance.cost < 0:
        raise ValidationError("Цена не может быть отрицательной!")


@receiver(pre_save, sender=Group)
def check_group(sender, instance, **kwargs):
    product_start_date = instance.product.start_date
    if timezone.now() > product_start_date:
        raise ValidationError("Вы опоздали, продукт уже начался!")
    if instance.min_users > instance.max_users:
        raise ValidationError(
            "Минимальное количество пользователей не может быть больше максимального!"
        )
    if instance.max_users < instance.min_users:
        raise ValidationError(
            "Максимальное количество пользователей не может быть меньше минимального!"
        )
    if instance.min_users < 0:
        raise ValidationError(
            "Минимальное количество пользователей не может быть меньше нуля!"
        )
    if instance.max_users < 0:
        raise ValidationError(
            "Максимальное количество пользователей не может быть меньше нуля!"
        )


@receiver(pre_save, sender=GroupMembership)
def check_group_membership(sender, instance, **kwargs):
    group = instance.group
    count_users = GroupMembership.objects.filter(group=instance.group).count()
    if count_users >= group.max_users:
        raise ValidationError(
            "Превышено максимальное количество пользователей в группе!"
        )
