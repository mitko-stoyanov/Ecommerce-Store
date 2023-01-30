from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from online_store.orders.models import Order


@receiver(pre_save, sender=Order)
def my_callback(sender, instance, **kwargs):
    try:
        old_instance = Order.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            message = render_to_string('orders/changed_status_email.html',
                                       {
                                           'order': instance,
                                       })
            send_mail(
                'Статусът е променен',
                message,
                None,
                [old_instance.user.email],
            )
    except Order.DoesNotExist:
        pass
