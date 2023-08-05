from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings as store_settings
from ob_dj_store.core.stores.models import Cart, Category, Order, OrderHistory, Wallet
from ob_dj_store.utils.utils import resize_image


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_customer_cart_and_wallet_handler",
)
def create_customer_cart_and_wallet_handler(sender, instance, created, **kwargs):
    if not created:
        return
    cart = Cart(customer=instance)
    cart.save()
    country = getattr(instance, "country", None)
    Wallet.objects.create(user=instance, country=country)


# add receiver to ProductVariant to create inventory


@receiver(
    post_save,
    sender=Order,
    dispatch_uid="create_order_history_handler",
)
def create_order_history_handler(sender, instance, created, **kwargs):
    OrderHistory.objects.create(
        order=instance,
        status=instance.status,
    )


@receiver(
    post_save,
    sender=Category,
    dispatch_uid="create_category_thumbnails",
)
def create_media_thumbnails(sender, instance, created, **kwargs):
    medium_dim = getattr(store_settings, "THUMBNAIL_MEDIUM_DIMENSIONS", None)
    small_dim = getattr(store_settings, "THUMBNAIL_SMALL_DIMENSIONS", None)
    if instance.image:
        if medium_dim:
            instance.image_thumbnail_medium = resize_image(
                instance.image, dim=medium_dim, size_name="medium"
            )
        if small_dim:
            instance.image_thumbnail_small = resize_image(
                instance.image, dim=small_dim, size_name="small"
            )
