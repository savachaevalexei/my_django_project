from django.utils import timezone
from django.conf import settings



# Формируем меню
menu = [
    {'title': "Свежее", 'url_name': 'home', 'class': 'fa fa-bolt fa-fw'},
    {'title': "Избранное", 'url_name': 'bookmarks', 'class': 'fa fa-bookmark fa-fw'},
    {'title': "Категории", 'url_name': 'cat', 'class': 'fa fa-bars fa-fw'},
    {'title': "Добавить статью", 'url_name': 'add_post', 'class': 'fa fa-pencil  fa-fw'},
    {'title': "О сайте", 'url_name': 'about', 'class': 'fa fa-info  fa-fw'},
    # {'title': "Мероприятия", 'url_name': 'events', 'class': 'fa fa-users fa-fw'},
    # {'title': "Вакансии", 'url_name': 'vacancy', 'class': 'fa fa-address-card-o fa-fw'},
]


class DataMixin:
    # Количество записей на странице (пагинация)
    
    paginate_by = 5
    title_page = None

    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE,
                     }

    def __init__(self):
        # Получаем название стрицы из переменной title_page
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu
        
        # Получаем текущую дату
        self.extra_context['today_date'] = timezone.now().date()

    

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['bookmark_list'] = None
        context['like_list'] = None
        context['menu'] = menu
        context['cat_selected'] = None
        context['sub_categories'] = None
        context['comments'] = None
        context.update(kwargs)
        return context
