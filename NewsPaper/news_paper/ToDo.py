from celery import shared_task

import django.contrib.auth
from .models import Post, Subs_sender
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from datetime import datetime, timedelta


@shared_task
def send_mail(post_id, mailing):
    post = Post.objects.get(id=post_id)

    html_content = render_to_string(
        'mailing.html',
        {
            'post': post,
            'text': post.priview(),
            'username': mailing["subscribers__username"],
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post.title}',
        body=f'Здравствуйте, {mailing["subscribers__username"]}. '
        'Новая статья в твоём любимом разделе!',
        from_email='testowitch.i@yandex.ru',
        to=[mailing['subscribers__email']],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@shared_task
def do_mailing():
    end_date = datetime.now().replace(hour=6, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)

    for person in django.contrib.auth.get_user_model().objects.all():
        send_post = Post.objects.filter(
            creation_time__range=(start_date, end_date),
            categories__in=Subs_sender.objects.filter(subscribers=person).
            values('category')
            )
        if send_post:
            html_content = render_to_string(
                'mailing_list.html',
                {
                    'post': send_post,
                    'user': person,
                }
            )

            posts_list_txt = ', '.join([post.title for post in send_post])
            msg = EmailMultiAlternatives(
                subject='Список новых статей',
                body=f'Здравствуй, {person.username}.'
                f'Список новых статей за неделю:'
                f'{posts_list_txt}',
                from_email='testowitch.i@yandex.ru',
                to=[person.email],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()