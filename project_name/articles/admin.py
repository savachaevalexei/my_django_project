from django.contrib import admin, messages
from .models import Article, Category, TagPost
from django.utils.safestring import mark_safe


# Настройки админ-панели для модели Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    fields = ['title', 'slug', 'description', 'prewiew_img', 'post_photo',  'content', 'meta_description', 'meta_keywords', 'status_moderate', 'is_published', 'cat', 'tags','difficulty', 'time_to_read', 'author']
    # Делаем поля slug, post_photo только для чтения
    readonly_fields = ['slug', 'post_photo']
    # Изменяем внешний вид виджета для выбора тэгов
    filter_horizontal = ['tags']
    # Поля для отображения
    list_display = ('id', 'title', 'time_create', 'status_moderate', 'is_published', 'cat','difficulty', 'time_to_read', 'author',)  
    # Поля которые будут кликабельны
    list_display_links = ('id', 'title')  
    # Сортировка по дате или заголовку, если есть статьи у которых дата добавления одинаковая
    ordering = ['-time_create', 'title']
    # Поле которое можно будет отредактировать, не переходя к редактированию всей записи
    list_editable = ('is_published', 'status_moderate',)
    # Пагинация - число отображаемых записей на странице
    list_per_page = 10  
    # Добавить новое действие
    actions = ['set_published', 'set_draft']  
    # Добавить поиск по полю title и полю name связанной таблицы Category
    search_fields = ['title', 'cat__name']
    # Добавляем фильтры
    list_filter = ['cat__name', 'is_published']  
    # Добавить панель сохранения измнений в начало страницы
    save_on_top = True  

    # Метод для получения изображения
    @admin.display(description="Выбранное изображение для превью")
    def post_photo(self, articles: Article):
        if articles.prewiew_img:
            return mark_safe(f"<img src='{articles.prewiew_img.url}' width=500>")
        return "Без фото"
    

    # Действие - Опубликовать
    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Article.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    # Действие - Снять с публикации
    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Article.Status.DRAFT)
        self.message_user(
            request, f"{count} записей снято с публикации.", messages.WARNING)





# Настройки админ-панели для модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name','description', 'slug','img', 'post_photo')
    readonly_fields = ['slug', 'post_photo']  # Делаем поле slug только для чтения
    list_display = ('name', 'post_photo')
    list_display_links = ('name',)
    ordering = ['-name']

    # Метод для получения изображения
    @admin.display(description="Изображение")
    def post_photo(self, articles: Category):
        if articles.img:
            return mark_safe(f"<img src='{articles.img.url}' width=100>")
        return "Без фото"




# Настройки админ-панели для модели TagPost
@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']  # Делаем поле slug только для чтения
    list_display = ('tag', 'slug')
    list_display_links = ('tag',)
    ordering = ['-tag']
