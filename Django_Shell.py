from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment



def django_shell():
    # создание пользователей для сайта
    ilya_user = User.objects.create_user(username='ilya', email='ilya@gmail.com')
    vlad_user = User.objects.create_user(username='vlad', email='vlad@gmail.com')

    # создаем модели авторов
    ilya = Author.objects.create(user=ilya_user)
    vlad = Author.objects.create(user=vlad_user)

    # категории
    cat_music = Category.objects.create(name="Музыка")
    cat_food = Category.objects.create(name="Еда")
    cat_movies = Category.objects.create(name="Фильмы")
    cat_games = Category.objects.create(name="Игры")


    # создание текстов статей/новостей
    article_food_movies = """статья_еда_кино_Ильи__статья_еда_кино_Ильи__статья_еда_кино_Ильи__
                             статья_еда_кино_Ильи__статья_еда_кино_Ильи__"""

    article_games = """статья_игры_Влада__статья_игры_Влада__статья_игры_Влада__статья_игры_Влада__
                       статья_игры_Влада__статья_игры_Влада__"""

    news_music = """новость_музыки_Ильи__новость_музыки_Ильи__новость_музыки_Ильи__новость_музыки_Ильи__
                        новость_музыки_Ильи__новость_музыки_Ильи__"""

    # создание двух статей и новости
    article_ilya = Post.objects.create(author=ilya, post_type=Post.article, title="статья_еда_кино_Ильи",
                                        text=article_food_movies)
    article_vlad = Post.objects.create(author=vlad, post_type=Post.article, title="статья_игры_Влада",
                                        text=article_games)
    news_ilya = Post.objects.create(author=ilya, post_type=Post.news, title="новость_музыки_Ильи", text=news_music)


    # назначение категорий этим объектам
    PostCategory.objects.create(post=article_ilya, category=cat_movies)
    PostCategory.objects.create(post=article_ilya, category=cat_food)
    PostCategory.objects.create(post=article_vlad, category=cat_games)
    PostCategory.objects.create(post=news_ilya, category=cat_music)

    # создание комментариев
    comment1 = Comment.objects.create(post=article_ilya, user=vlad.user, text="комментарий Влада №1 к статье Ильи")
    comment2 = Comment.objects.create(post=article_vlad, user=ilya.user, text="комментарий Ильи №2 к статье Влада")
    comment3 = Comment.objects.create(post=news_ilya, user=ilya.user, text="комментарий Ильи №3 к новости Ильи")
    comment4 = Comment.objects.create(post=news_ilya, user=vlad.user, text="комментарий Влада №4 к новости Ильи")

    # объекты для оценки
    like_dislike = [article_ilya, article_vlad, news_ilya, comment1, comment2, comment3, comment4]

    like_dislike[1].like()
    like_dislike[0].dislike()
    like_dislike[3].like()
    like_dislike[4].like()

    # рейтинг Ильи
    rating_ilya = (sum([post.rating * 3 for post in Post.objects.filter(author=ilya)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=ilya.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=ilya)]))
    ilya.update_rating(rating_ilya)

    # рейтинг Влада
    rating_vlad = (sum([post.rating * 3 for post in Post.objects.filter(author=vlad)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=vlad.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=vlad)]))
    vlad.update_rating(rating_vlad)

    # Выявляем лучшего из двоих
    best_author = Author.objects.all().order_by('-rating')[0]

    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")

    # выявляем лучшую статью
    best_article = Post.objects.filter(post_type=Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.created)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")

    # отображаем вск комментарии к статье
    print("Комментарии к ней")
    for com in Comment.objects.filter(post=best_article):
        print("Дата:", com.created)
        print("Автор:", com.user.username)
        print("Рейтинг:", com.rating)
        print("Комментарий:", com.text)
        print("")