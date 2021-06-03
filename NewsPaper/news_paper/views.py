from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,\
    CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin

from .models import Author, Category, Post, PostCategory, Subs_sender
from .filters import PostFilter
from .forms import PostForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model



class NewsList(ListView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'news_id'
    ordering = '-created_data'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name='authors').exists()
        return context


class NewsCategoryList(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'category'
    ordering = '-created_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Post.objects.filter(categories__id=self.kwargs['pk'])
        context['category'] = qs
        context['category_name'] = Category.objects.get(id=self.kwargs['pk'])
        sub = list(Subs_sender.objects.filter(subscribers=self.request.user.id).
                   values('category'))
        context['subscribed'] = [s['category'] for s in sub]
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = list(PostCategory.objects.filter(
            post=self.kwargs['pk']).values('category', 'category__category'))
        sub = list(Subs_sender.objects.filter(subscribers=self.request.user.id).
                   values('category'))
        context['subscribed'] = [s['category'] for s in sub]
        context['author_name'] = Post.objects.filter(id=self.kwargs['pk']).\
            values('author__user_id__username')[0]['author__user_id__username']
        return context


class PostsFiltered(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search_post'
    ordering = ['-created_data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class PostAdd(PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news_paper.add_post',)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news_paper.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def author_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.get_or_create(user_id=request.user)
    return redirect('/news')


@login_required
def subscribe_me(request, pk):
    if not Subs_sender.objects.check(subscribers=get_user_model().
                                 objects.get(id=request.user.id),
                                 category=Category.objects.get(id=pk)):
        Subs_sender.objects.create(subscribers=get_user_model().
                               objects.get(id=request.user.id),
                               category=Category.objects.get(id=pk))
    return redirect('/news')