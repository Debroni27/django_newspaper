from django.db import models
import django.contrib.auth

from django.core.cache import cache


class Author(models.Model):
    user_id = models.OneToOneField(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        comment_in_post_rating = 0
        comment_rating = 0
        for i in Post.objects.filter(author=self):
            post_rating += i.rating
            for n in Comment.objects.filter(post=i.id):
                comment_in_post_rating += n.rating

        for c in Comment.objects.filter(user=self.user_id):
            comment_rating += c.rating

        self.rating = post_rating*3 + comment_in_post_rating + comment_rating
        self.save()

    def __str__(self):
        return '{}'.format(self.user_id)


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class Post(models.Model):
    NEWS = 'N'
    ARTICLE = 'A'

    POST_TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPE, default=ARTICLE)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)
    created_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.title)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125] + ('...' if len(self.text) > 124 else '')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.get_user_model(),
                             on_delete=models.CASCADE)
    text = models.TextField(default='')
    created_data = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.category)


class Subs_sender(models.Model):
    subscribers = models.ForeignKey(django.contrib.auth.get_user_model(),
                                    on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.subscribers)





