from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-(t55gyyqc!m_j%pf__et)$#j55a^zcd5ijn#@nd-sdj!+)803t'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 
                 'b5e9-93-120-213-31.ngrok-free.app',
                 ]

CSRF_TRUSTED_ORIGINS=["https://b5e9-93-120-213-31.ngrok-free.app"] 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # 'debug_toolbar',
    "django_rename_app",
    'articles.apps.ArticlesConfig',
    'users.apps.UsersConfig',
    'tinymce',
    'captcha',
    'mptt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'project_name.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_articles_context',

            ],
        },
    },
]

WSGI_APPLICATION = 'project_name.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'

# Перенаправление на главную страницу после авторизации
LOGIN_REDIRECT_URL = 'home'

# Перенаправление на главную страницу после выхода из профиля
LOGOUT_REDIRECT_URL = 'home'

# Перенаправление на страницу авторизации 
LOGIN_URL = 'users:login'

AUTH_USER_MODEL = 'users.User'

# Бэкэнд для авторизации
AUTHENTICATION_BACKENDS = [
    # Авторизация по username
    'django.contrib.auth.backends.ModelBackend', 
    # Авторизация по email (логика в файле users/authrntication.py)
    'users.authentication.EmailAuthBackend',
]


TINYMCE_DEFAULT_CONFIG = {
    "height": "600px",
    "width": "100%",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code codesample "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft codesample"
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "ru_RU",
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Настройка почты
# EMAIL_HOST = "smtp.yandex.ru"
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "djangocourse@yandex.ru"
# EMAIL_HOST_PASSWORD = " bnufhkwcripaunvu"
# EMAIL_USE_SSL = True

# Для отправки почты от имени приложения
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# SERVER_EMAIL = EMAIL_HOST_USER
# EMAIL_ADMIN = EMAIL_HOST_USER

CAPTCHA_IMAGE_SIZE=[160,80]
