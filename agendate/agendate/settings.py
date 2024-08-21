import os
from pathlib import Path
from decouple import config
import firebase_admin
from firebase_admin import credentials



# Asegúrate de que SESSION_ENGINE esté correctamente configurado
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

OPENAI_API_KEY = config('OPENAI_API_KEY')

# Inicializa Firebase
cred_path = config('FIREBASE_CREDENTIALS_PATH', default='/home/user/agendate4mentes/focal-elf-388317-firebase-adminsdk-y7osn-aec3a8ce26.json')
cred = credentials.Certificate(cred_path)
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass  # Firebase app ya inicializado

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para Django
SECRET_KEY = config('SECRET_KEY', default='django-insecure-_$8*421gbuthxjx^-i+c)v5+pc2az*&x4d!hxtg$-z28&+zpfz')

# Modo depuración - Cambia a False en producción
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'focal-elf-388317.web.app', 
    'focal-elf-388317.firebaseapp.com'
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://focal-elf-388317.web.app",
    "https://focal-elf-388317.firebaseapp.com",
]

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# Configuración de URLs principales
ROOT_URLCONF = 'agendate.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI application
WSGI_APPLICATION = 'agendate.wsgi.application'

# Configuración de la base de datos (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de la autenticación
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'


# Configuración adicional para OPTIONS
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',
    'PUT',
    'PATCH',
    'DELETE'
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'x-csrftoken',
    'authorization',
    'accept',
    'origin',
    'x-requested-with'
]

# Configuración de Firebase
FIREBASE_CONFIG = {
    "apiKey": config("FIREBASE_API_KEY"),
    "authDomain": config("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": config("FIREBASE_DATABASE_URL"),
    "projectId": config("FIREBASE_PROJECT_ID"),
    "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": config("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": config("FIREBASE_APP_ID"),
}

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
}
