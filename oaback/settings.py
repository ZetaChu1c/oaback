"""
Django settings for oaback project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s9vp8=qt4mgw2*u0w3$kumx^gsc2^-f!y92&kn2z)&s6df68^j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    "django.contrib.staticfiles",
    # 安装rest_framework
    "rest_framework",
    # 配置跨域访问
    "corsheaders",
    # 注册应用
    "apps.oaauth",
    "apps.absent",
    "apps.inform",
    "apps.staff",
    "apps.image",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    # 配置跨域访问,要配置在会生成响应的中间件之前
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 关闭csrf验证
    # "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 自定义中间件
    "apps.oaauth.middlewares.LoginCheckMiddleware",
]

ROOT_URLCONF = "oaback.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                # "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "oaback.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": env.str('DB_NAME', 'ctos'),
        "USER": env.str('DB_USER', "root"),
        "PASSWORD": env.str("DB_PASSWORD", "9523"),
        "HOST": env.str('DB_HOST', 'localhost'),
        "PORT": env.str('DB_PORT', 3306),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# 修改语言编码
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "UTC"

USE_I18N = True

# 修改时区为False，不启用时区
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = BASE_DIR / "media"
# http://127.0.0.1:8000/media/abc.png
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 允许所有域名跨域访问
CORS_ALLOW_ALL_ORIGINS = True

# 覆盖django自带的User模型
AUTH_USER_MODEL = "oaauth.OAUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.oaauth.authentications.UserTokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

APPEND_SLASH = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "1308698143@qq.com"
EMAIL_HOST_PASSWORD = "yybrcpqjgbrnjefi"
DEFAULT_FROM_EMAIL = "1308698143@qq.com"


# CELERY相关配置
# 中间人的配置
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/1')
# 指定结果的接受地址
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/2')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


# 缓存设置
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.str('CACHE_URL', "redis://127.0.0.1:6379/3"),
    }
}

LOGGING = {
    "version": 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
       'file': {
           'level': 'DEBUG',
           'class': 'logging.FileHandler',
           'filename': '/data/log/oa.log',
           'formatter': 'verbose'
       },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'level': 'DEBUG',
        },
    },
}