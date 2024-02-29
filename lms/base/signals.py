from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from .models import Product


@receiver(post_save, sender=Product)
def create_product_group(sender, instance, created, **kwargs):
    if created:
        group_name = instance.name.lower().replace(" ", "_")
        group, created = Group.objects.get_or_create(name=group_name)

        permission = Permission.objects.get(codename="view_product")
        group.permissions.add(permission)
        group.save()
