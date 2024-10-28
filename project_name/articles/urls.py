from django.urls import path
from . import views



urlpatterns = [

    # Главная страница
    path('', views.SiteHome.as_view(), name='home'),

    # Страница - Избранное 
    path('bookmarks/', views.UserBookmarks.as_view(), name='bookmarks'),

    # Удалить комментарий
    path('delete_comment/', views.delete_comment, name='delete_comment'),

    # Добавить в избранное
    path('add_bookmark/', views.add_bookmark, name='add_bookmark'),

    # Удалить из избранного
    path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),

    # Поставить лайк
    path('add_like/', views.add_like, name='add_like'),

    # Удалить лайк
    path('delete_like/', views.delete_like, name='delete_like'),

    # Страница вывода всех возможных категорий
    path('cat', views.ShowAllCategory.as_view(), name='cat'),

    # Подписаться на категорию
    path('sub_category/', views.subscribe_category, name='sub_category'),

    # Отписаться от категории
    path('unsub_category/', views.unsubscribe_category, name='unsub_category'),

    # Страница - Мероприятия 
    path('events/', views.SiteEvents.as_view(), name='events'),

    # Страница - Вакансии 
    path('vacancy/', views.SiteVacancy.as_view(), name='vacancy'),

    # Страница - Вакансии 
    path('about/', views.SiteAbout.as_view(), name='about'),

    # Страница вывода содержания статьи
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),

    # Страница вывода статей, отобранных по названию категории
    path('category/<slug:cat_slug>/', views.ShowPostByCategory.as_view(), name='category'),
        
    # Страница вывода статей, отобранных по тэгу
    path('tag/<slug:tag_slug>/', views.ShowPostByTag.as_view(), name='tag'),
    
    # Страница добавления статьи для пользователя
    path('add_post/', views.AddPage.as_view(), name='add_post'),
    
    # Спасибо, за публикацию
    path('th_add_post/', views.ThAddPost.as_view(), name='th_add_post'),

    # Поиск по сайту
    path('search/', views.SearchResultsView.as_view(), name='search_results'),


]