from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment, Subs_sender


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating')
    list_filter = ('categories', 'type', 'created_data')
    search_fields = ('author', 'categories__name')

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subs_sender)
