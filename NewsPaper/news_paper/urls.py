from django.urls import path
from .views import NewsList, NewsDetail, PostsFiltered, PostAdd, PostEdit,\
    PostDelete, author_me, subscribe_me, NewsCategoryList
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('',cache_page(60)(NewsList.as_view())),
    path('<int:pk>', NewsDetail.as_view(), name='detail_news'),
    path('category/<int:pk>/', cache_page(60*5)(NewsCategoryList.as_view()),
         name='category'),
    path('search/', PostsFiltered.as_view()),
    path('add/', PostAdd.as_view(), name='news_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('setauthor/', author_me, name='author_me'),
    path('<int:pk>/subscribe/', subscribe_me, name='subscribe_category'),
]