from .models import PostCategory, Subs_sender

from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from .ToDo import send_mail


@receiver(m2m_changed, sender=PostCategory)
def do_mailing(sender, action, instance, **kwargs):
    if action == 'post_add':
        category_lst = list(sender.objects.filter(post=instance.id).
                            values('category'))
        for category in category_lst:
            mailing_list = list(Subs_sender.objects.filter(
                category=category['category']).values('subscribers__username',
                                                      'subscribers__email'))
            for mail in mailing_list:

                send_mail.delay(instance.id, mail)