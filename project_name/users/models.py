from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

# Функция для транслитерации
def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

EMPLOYMENTSTATUS = (
            ('Ищу работу', 'Ищу работу'),
            ('Трудоестроен', 'Трудоеустроен'),
        )



class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    specialization = models.CharField(max_length=255, verbose_name="Технологическая специализация")
    country_of_residence = models.CharField(max_length=255, verbose_name="Страна проживания")
    city_of_residence = models.CharField(max_length=255, verbose_name="Город проживания")
    website = models.CharField(max_length=255, verbose_name="Ссылка на сайт")
    github = models.CharField(max_length=255, verbose_name="Ссылка на профиль GitHub")
    education = models.CharField(max_length=255, verbose_name="Образование")
    employment_status = models.CharField(max_length=255,choices=EMPLOYMENTSTATUS, verbose_name="Трудовой статус")
    place_of_work = models.CharField(max_length=255, verbose_name="Место работы")
    work_experience = models.TextField(blank=True, verbose_name="Опишите опыт работы: где, сколько и кем работали")
    courses = models.TextField(blank=True, verbose_name="Перечислите курсы, которые проходили")
    skills = models.CharField(max_length=255, verbose_name="Перечислите через запятую hard и soft skills, которыми владете")
    about_me = models.TextField(blank=True, verbose_name="Расскажите о себе")
    hobby = models.CharField(max_length=255, verbose_name="Перечислите через запятую хобби, которыми увлекаетесь")
    publications = models.TextField(blank=True, verbose_name="Публикации")
    foreign_languages = models.ManyToManyField('ForeignLanguagesList', blank=True, related_name='foreign_languages', verbose_name="Перечислите через запятую языки, которыми владеете")


class ForeignLanguagesList(models.Model):
    language = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta():
        verbose_name = "Иностранные языки"
        verbose_name_plural = "Иностранные языки"

    def __str__(self):
        return self.language

    # Метод для автоматического формирования слага
    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.language))
        super().save(*args, **kwargs)