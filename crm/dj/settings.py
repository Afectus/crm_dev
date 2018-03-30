import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rf1sld^3prplbp%cie#9zdenydvh9=9x^phn+gxaw_3et6$s9w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
	#misha
	'report3',
	'softapp',
	'deliveryapp',
	#algol
	'accountstorage',
	'project',
	'report2',
	'instructions',
	'normact',
	'telegramtemplate',
	'corpmail',
	'materialvalue',
	'organizer',
	'pictgallery',
	'useridea2',
	'newsfeed',
	'docflow',
	#
	'testtest',
	#1c
	'api1c',
	#
	'notify',
	'workgraph',
	'holiday',
	'projects',
	'personal',
	'report',
	'inventory',
	'kassir',
	'opt',
	'bizprocess',
	#
	'userauth',
	'acl',
	'it',
	'log',
	'order',
	'node',
	'panel',
	'sms',
	'call',
	'device',
	'screen',
	'screen1',
	'screen2',
	'video',
	'bitrix',
	'mod',
	'workflow',
	'pricetag',
	'worktask',
	'useridea',
	'marketing',
	'library',
	#
	'rest_framework',
	'captcha',
	'imagekit',
	'ckeditor',
	'corsheaders', #django-cors-headers
	'django_unused_media',
	#'django_cleanup',
	#'locale',
	'django_extensions',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.postgres', #for *.objects.filter(search__*='*')
	#
	'aldjemy',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	#django-cors-headers
	'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'dj.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['template',],
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

WSGI_APPLICATION = 'dj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2', #'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'crm',
		'USER': 'crm',
		'PASSWORD': 'crm',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	}
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = (
	('ru', u'Русский'),
	#('en', 'English'),
)

TIME_ZONE ='Asia/Krasnoyarsk'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_INPUT_FORMATS = ['%d-%m-%y','%d-%m-%Y']

LOGIN_URL = '/user/login'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

try:
	from dj.settings_local import STATICFILES_DIRS
except:
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, "static")
CKEDITOR_CONFIGS = {
	'default': {
	'toolbar': [
	['Undo', 'Redo',
	'-', 'Bold', 'Italic', 'Underline',
	'-', 'Link', 'Unlink', 'Anchor', 'Image',
	'-', 'Format',
	'-', 'SpellChecker', 'Scayt',
	'-', 'Maximize',
	'-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock',
	],
	['HorizontalRule',
	'-', 'Table',
	'-', 'BulletedList', 'NumberedList',
	'-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
	'-', 'SpecialChar',
	'-', 'Source',
	]
	],
}
}


#CATCHA SETTINGS
CAPTCHA_FONT_SIZE = 40
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_FOREGROUND_COLOR = '#ff6600'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_LETTER_ROTATION = (-1, 1)
########################


REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.BasicAuthentication',
		#'rest_framework.authentication.SessionAuthentication',
	)
}


try:
	from dj.settings_local import *
except:
	pass
