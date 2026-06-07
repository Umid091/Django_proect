from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GalleryImage

print("signale failli o'qildi")


from django.db.models.signals import post_delete

@receiver(post_delete, sender=GalleryImage)
def announce_deleted_image(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "gallery_group",
        {
            "type": "delete_image",
            "id": instance.id
        }
    )

@receiver(post_save, sender=GalleryImage)
def announce_new_image(sender, instance, created, **kwargs):
    print("+++++++++++signal ishladi++++++++++++++++++++++++++++++++")
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gallery_group",
            {
                "type": "send_image",
                "image_url": instance.image.url,
                "id": instance.id
            }
        )


from django.db.models.signals import post_save


@receiver(post_save, sender=GalleryImage)
def announce_image_change(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    action = 'create' if created else 'update'

    async_to_sync(channel_layer.group_send)(
        "gallery_group",
        {
            "type": "send_image_update",
            "action": action,
            "id": instance.id,
            "image_url": instance.image.url
        }
    )