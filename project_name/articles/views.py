from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Article, TagPost, Category, Bookmark, Like, SubscibeCategories, Comments
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from .utils import DataMixin
from .forms import AddPostForm, AddCommentForm
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
        
# Главная страница
class SiteHome(DataMixin, ListView):

    template_name = 'articles/index.html'
    context_object_name = 'posts'
    title_page = 'Свежее'
    cat_selected = 0
    

    def get_context_data(self, *, object_list=None, **kwargs):
        
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            # Получаем id статей, которые user добавил в закладки 
            bookmark_list = Bookmark.objects.filter(user=self.request.user).values_list('article', flat=True)
            like_list = Like.objects.filter(user=self.request.user).values_list('article', flat=True)
            comments = Comments.objects.all().values_list('article', flat=True)
            return self.get_mixin_context(context, bookmark_list=bookmark_list, like_list=like_list, comments=comments)
        
        else:
            comments = Comments.objects.all().values_list('article', flat=True)
            context = super().get_context_data(**kwargs)
            return self.get_mixin_context(context, comments=comments)

        
    def get_queryset(self):
        return Article.published.all().select_related('cat')
    
    

# Страница - Избранное 
class UserBookmarks(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'articles/bookmarks.html'
    context_object_name = 'bookmarks'
    title_page = 'Избранное'

    def get_context_data(self, *, object_list=None, **kwargs):
        
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            sub_categories = SubscibeCategories.objects.filter(user=self.request.user).values_list('name', flat=True)
            return self.get_mixin_context(context, sub_categories=Category.objects.filter(pk__in=sub_categories))
        
        else:
            context = super().get_context_data(**kwargs)
            return self.get_mixin_context(context)


    # Выводим избранные статьи
    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(user=self.request.user).values_list('article', flat=True)
   
        return Article.objects.filter(pk__in=bookmarks)
    
    
# Добавление статьи в избранное 
def add_bookmark(request):
    article = Article.objects.get(pk=request.GET.get('article_id'))
    user = request.user
    bookmark = Bookmark(article=article, user=user)
    bookmark.save()

    return HttpResponseRedirect('/')


# Удаление статьи из избранного 
def delete_bookmark(request):
    article = Article.objects.get(pk=request.GET.get('article_id'))
    user = request.user
    bookmark = Bookmark.objects.get(article=article, user=user)
    bookmark.delete()

    return HttpResponseRedirect('/')
                        
# Поставить лайк
def add_like(request):
    article = Article.objects.get(pk=request.GET.get('article_id'))
    user = request.user
    like = Like(article=article, user=user)
    like.save()

    return HttpResponseRedirect('/')


# Удалить лайк
def delete_like(request):
    article = Article.objects.get(pk=request.GET.get('article_id'))
    user = request.user
    like = Like.objects.get(article=article, user=user)
    like.delete()

    return HttpResponseRedirect('/')
                                               
# Страница - Категории
class ShowAllCategory(DataMixin, ListView):
    template_name = 'articles/categories.html'
    context_object_name = 'categories'
    title_page = 'Категории'
    cat_selected = 0
    paginate_by = False
    
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE,
                     }
    
    def get_context_data(self, *, object_list=None, **kwargs):

        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            sub_categories = SubscibeCategories.objects.filter(user=self.request.user).values_list('name', flat=True)
            return self.get_mixin_context(context, sub_categories=sub_categories)
        else:
            context = super().get_context_data(**kwargs)
            return self.get_mixin_context(context)


    def get_queryset(self):
        # Возвращаем все возможные категории из БД
        return Category.objects.all()
    
    
# Подписаться на категорию
def subscribe_category(request):
    cat = Category.objects.get(pk=request.GET.get('cat_id'))
    user = request.user
    like = SubscibeCategories(name=cat, user=user)
    like.save()

    return HttpResponseRedirect('/')


# Отписаться от категории
def unsubscribe_category(request):
    cat = Category.objects.get(pk=request.GET.get('cat_id'))
    user = request.user
    like = SubscibeCategories.objects.get(name=cat, user=user)
    like.delete()

    return HttpResponseRedirect('/')


# Страница - Мероприятия 
class SiteEvents(DataMixin, ListView):
    template_name = 'articles/events.html'
    context_object_name = 'posts'
    title_page = 'Мероприятия'

    def get_queryset(self):
        # !!!!!!!!!!!!!!!!!!ВРЕМЕННО!!!!!!!!!!
        return Article.published.all().select_related('cat')

# Страница - Вакансии 
class SiteVacancy(DataMixin, ListView):
    template_name = 'articles/vacancy.html'
    context_object_name = 'posts'
    title_page = 'Вакансии'

    def get_queryset(self):
        # !!!!!!!!!!!!!!!!!!ВРЕМЕННО!!!!!!!!!!
        return Article.published.all().select_related('cat')


# Страница - О сайте 
class SiteAbout(DataMixin, ListView):
    template_name = 'articles/about.html'
    context_object_name = 'posts'
    title_page = 'Вакансии'

    def get_queryset(self):
        # !!!!!!!!!!!!!!!!!!ВРЕМЕННО!!!!!!!!!!
        return Article.published.all().select_related('cat')
    

# Вывод полного содержания статьи
class ShowPost(DataMixin, DetailView, CreateView):
    template_name = 'articles/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = AddCommentForm


    def get_context_data(self, *, object_list=None, **kwargs):     
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            bookmark_list = Bookmark.objects.filter(user=self.request.user).values_list('article', flat=True)
            like_list = Like.objects.filter(user=self.request.user).values_list('article', flat=True)
            comments = Comments.objects.all().values_list('article', flat=True)
            
            return self.get_mixin_context(context, bookmark_list=bookmark_list, like_list=like_list, comments=comments)
                                         
        else:
            comments = Comments.objects.all().values_list('article', flat=True)
            context = super().get_context_data(**kwargs)
            return self.get_mixin_context(context, title=context['post'].title, comments=comments)

  

    def post(self, request, **kwargs):
        if request.method == 'POST':
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = Article.objects.get(slug=self.kwargs[self.slug_url_kwarg])
                comment.author = self.request.user
                comment.save()
                return redirect('/')
        else:
            form = AddCommentForm()  
        return render(
            request,
            self.template_name,
            { 'form': form}
        )    
    
    # Выбираем только те статьи, которые имеют статус "опубликованно", иначе генерируем 404
    def get_object(self, queryset=None):
        return get_object_or_404(Article.published, slug=self.kwargs[self.slug_url_kwarg])

# Удалить комментарий
def delete_comment(request):
    user = request.user
    id = request.GET.get('comment_id')
    comment = Comments.objects.get(pk=id, author_id=user)
    comment.delete()
    Comments.objects.filter(parent_id=id).update(parent_id=0)
    
    return HttpResponseRedirect('/')    



# Вывод статей, отобранных по названию категории
class ShowPostByCategory(DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            sub_categories = SubscibeCategories.objects.filter(user=self.request.user).values_list('name', flat=True)
            cat = context['posts'][0].cat
            return self.get_mixin_context(context, cat_selected=cat.pk,sub_categories=sub_categories)
        
        else:
            context = super().get_context_data(**kwargs)
            cat = context['posts'][0].cat
            return self.get_mixin_context(context, cat_selected=cat.pk)

    def get_queryset(self):
        return Article.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


# Вывод статей, отобранных по тегу
class ShowPostByTag(DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context)

    def get_queryset(self):
        return Article.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


# Добавление статьи
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'articles/add_post.html'
    title_page = 'Добавление статьи'
    success_url = '/th_add_post'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


# Спасибо, за публикацию
class ThAddPost(DataMixin, ListView):
    template_name = 'articles/th_add_post.html'
    context_object_name = 'posts'
    title_page = 'Спасибо!'

    def get_queryset(self):
        # !!!!!!!!!!!!!!!!!!ВРЕМЕННО!!!!!!!!!!
        return Article.published.all().select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("СТРАННИЦА НЕ НАЙДЕНА")


# Поиск по сайту
class SearchResultsView(ListView):
    model = Article
    template_name = 'articles/search_results.html'
 
    def get_queryset(self): # новый
        query = self.request.GET.get('q').lower()
       
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list

