"""
Django settings for sourcepro2 project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from pathlib import Path
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
print("BASE_DIRRRRRRRRR", BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '25hvcpi(fa3liem*9qj$@slda5kh7cy539@11_e6de$mkx@8g)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['sourceproenv.eba-mi9yupsf.us-west-2.elasticbeanstalk.com', '127.0.0.1','65.0.154.172','192.168.29.74',]
ALLOWED_HOSTS = ['172.31.2.182','3.109.9.214','192.168.29.220','127.0.0.1']
#,'192.168.214.147','192.168.212.147','192.168.212.16','192.168.57.147','192.168.57.16','3.110.168.213',


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'sourcepro',
    'django_celery_results',
    'django_celery_beat',


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]
#


#same origin settings starts here-----------
CORS_ALLOWED_ORIGINS = [

    'http://localhost:3000',
    'http://192.168.29.74:3000',
    # 'http://192.168.29.220:8000',





    ]

CORS_ALLOW_CREDENTIALS=True
#------same origin settings ends here-------



# CORS_ORIGIN_WHITELIST = (
#         'http://localhost:3000',
#         'http://3.110.105.9:3000',
#         'http://192.168.29.74:3000',
#         'http://192.168.0.106:3000',
#     )

# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_ALL_ORIGINS = True
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SAMESITE = 'None'
# SESSION_COOKIE_SAMESITE = 'None'

# SESSION_COOKIE_HTTPONLY=True
# CSRF_COOKIE_HTTPONLY=True


# CSRF_COOKIE_SAMESITE = 'None'
# SESSION_COOKIE_SAMESITE = 'None'
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True
# CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']
#
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
# ]
# CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
# CORS_ALLOW_CREDENTIALS = True
#
#
#

ROOT_URLCONF = 'sourcepro2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'build')],
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sourcepro2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'SPDB',
#         'USER': 'rockwell',
#         'PASSWORD': 'Rock_well123',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#    }
#
# }

# DATABASES = {
#     'default': {
#         'ENGINE':'django.db.backends.mysql',
#         'NAME':'sourcepro_db',
#         'USER':'ubuntu',
#         'PASSWORD':'SourceProDB$v01',
#         'HOST':'sourcepro-db.cbglvxe7ht7f.ap-south-1.rds.amazonaws.com',
#         'PORT':'3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME':'Sourcepro_New_DB',
        'USER':'vivek_aws',
        'PASSWORD':'Am@c1502',
        'HOST':'65.0.154.172',
        'PORT':'5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'build/static'),

]




# STATIC_ROOT= os.path.join(BASE_DIR, 'static') # settings affected at Deployment

#-----below static files dirs affect at development time
# STATICFILES_DIRS=[
#     os.path.join(BASE_DIR, "static_cdn"),
#     os.path.join('build','static'),
# ]


REST_FRAMEWORK = {
    # 'EXCEPTION_HANDLER': 'sourcepro.custom_exception_handler.custom_exception_handler',

    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',


    # ]
}












#email------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "neerajpynam@gmail.com"
EMAIL_HOST_PASSWORD = "tkekaspbkdfjanap"


#media---------------
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,"media/")



#celery----------
CELERY_BROKER_URL = 'redis://65.0.154.172:6379'  # Replace with your broker URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
# CELERY_RESULT_BACKEND = 'redis://65.0.154.172:6379/15'  # Replace with your result backend URL
CELERY_RESULT_BACKEND = 'django-db'





#celery beat-------------

CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'

print('^^^^ in settings ^^^^^^^')