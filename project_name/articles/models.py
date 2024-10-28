from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from users.models import User



# Функция для транслитерации
def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


# Пользовательский менеджер, который выводит только опубликованные записи
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Article.Status.PUBLISHED).filter(status_moderate=Article.StatusModerate.MODERATE)


# МОДЕЛЬ СТАТЬИ
class Article(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    class StatusModerate(models.IntegerChoices):
        DRAFT = 0, 'На модерации'
        MODERATE = 1, 'Проверено'


    DIFFICULTY = (
            ('Легкий', 'Легкая'),
            ('Средний', 'Средняя'),
            ('Сложный', 'Сложная'),
        )
    

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, verbose_name="Сложность")
    time_to_read = models.CharField(max_length=255, verbose_name="Время на чтение")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True, verbose_name="Краткое описание для превью")
    meta_description = models.TextField(blank=True, verbose_name="Мета описание")
    meta_keywords = models.TextField(blank=True, verbose_name="Мета теги")
    prewiew_img = models.ImageField(upload_to="article_prewiew_img/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Изображение для превью")
    content = HTMLField(blank=True, verbose_name="Текст",)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name="Статус публикации")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="posts", null=True, default=None)
    status_moderate = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), StatusModerate.choices)), default=StatusModerate.DRAFT, verbose_name="Статус модерации")


    objects = models.Manager()
    published = PublishedManager()


    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['time_create']),
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Метод для автоматического формирования слага
    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.title))
        super().save(*args, **kwargs)

    # Счетчик: сколько раз статью добавили в закладки
    def get_bookmark_count(self):
        return Bookmark.objects.filter(article=self).count()
    
    # Счетчик: сколько раз статью лайкнули
    def get_like_count(self):
        return Like.objects.filter(article=self).count()

# МОДЕЛЬ КАТЕГОРИИ
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(db_index=True, verbose_name="Описание категории")
    img = models.ImageField(upload_to="category_img/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Изображение")

    class Meta():
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    # Возвращает url для конкретной категории
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # Метод для автоматического формирования слага
    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.name))
        super().save(*args, **kwargs)


# МОДЕЛЬ ТЭГИ
class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta():
        verbose_name = "Тэги"
        verbose_name_plural = "Тэги"

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag

    # Метод для автоматического формирования слага
    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.tag))
        super().save(*args, **kwargs)


# МОДЕЛЬ ДЛЯ ЗАКЛАДОК
class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'article') 


# МОДЕЛЬ ДЛЯ ЛАЙКОВ
class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'article') 


# МОДЕЛЬ ДЛЯ ПОДПИСОК НА КАТЕГОРИИ
class SubscibeCategories(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'name') 

# МОДЕЛЬ ДЛЯ КОММЕНТАРИЕВ К СТАТЬЯМ
class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    parent_id = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    

        

