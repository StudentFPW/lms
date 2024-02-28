# from django.db.models.signals import post_save
# from django.dispatch import receiver


# @receiver(post_save, sender=Product)
# def distribute_users_to_groups(sender, instance, created, **kwargs):
#     if created:
#         product = instance.product
#         if product.start_date <= timezone.now():
#             # распределение пользователей в группы при начале продукта
#             distribute_users(product)
#         else:
#             # перераспределение групп для всех продуктов, чтобы обеспечить балансировку
#             balance_groups()
