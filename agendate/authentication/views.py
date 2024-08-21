from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import auth, credentials
import json
import logging

# Configura el log para la depuración
logger = logging.getLogger(__name__)

# Inicializa Firebase Admin SDK si no está ya inicializado
cred_path = '/home/user/agendate4mentes/focal-elf-388317-firebase-adminsdk-y7osn-aec3a8ce26.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                logger.debug("Campos de registro faltantes")
                return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

            if User.objects.filter(username=username).exists():
                logger.debug(f"El nombre de usuario {username} ya está en uso")
                return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

            if User.objects.filter(email=email).exists():
                logger.debug(f"El correo electrónico {email} ya está en uso")
                return JsonResponse({'error': 'El correo electrónico ya está en uso'}, status=400)

            # Registra al usuario en Firebase
            firebase_user = auth.create_user(email=email, password=password)
            logger.debug(f"Usuario registrado en Firebase: {firebase_user.uid}")

            # Crea el usuario en Django
            django_user = User.objects.create_user(username=username, email=email, password=password)
            logger.debug(f"Usuario creado en Django: {django_user.username}")

            return JsonResponse({'message': 'Usuario registrado exitosamente'})

        except json.JSONDecodeError:
            logger.error("Error al decodificar JSON en la solicitud de registro.")
            return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error en el registro: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_or_email = data.get('username_or_email')
            password = data.get('password')

            if not username_or_email or not password:
                logger.debug("Campos de autenticación faltantes")
                return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

            user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()

            if user is None:
                logger.debug("Usuario no encontrado")
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

            if not user.check_password(password):
                logger.debug("Contraseña incorrecta")
                return JsonResponse({'error': 'Contraseña incorrecta'}, status=400)

            auth_login(request, user)

            if request.user.is_authenticated:
                return JsonResponse({'message': 'Inicio de sesión exitoso', 'redirect_url': '/dashboard/'})
            else:
                return JsonResponse({'error': 'No se pudo autenticar al usuario'}, status=400)

        except json.JSONDecodeError:
            logger.error("Error al decodificar JSON en la solicitud de login.")
            return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error en el login: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'index.html')

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def logout(request):
    auth_logout(request)
    logger.debug("Usuario desautenticado y redirigido al login")
    return redirect('/')

@csrf_exempt
def forgotpassword(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                logger.debug("Correo electrónico faltante en solicitud de recuperación de contraseña")
                return JsonResponse({'error': 'El correo electrónico es requerido'}, status=400)

            # Enviar correo de restablecimiento de contraseña utilizando Firebase
            auth.send_password_reset_email(email)
            logger.debug(f"Correo de recuperación enviado a {email}")

            return JsonResponse({'message': 'Correo de recuperación enviado'})

        except json.JSONDecodeError:
            logger.error("Error al decodificar JSON en la solicitud de recuperación de contraseña.")
            return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error en la recuperación de contraseña: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def index(request):
    if request.user.is_authenticated:
        logger.debug(f"Usuario {request.user.username} ya autenticado, redirigiendo al dashboard")
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required
def dashboard(request):
    logger.debug(f"Accediendo al dashboard: {request.user}")
    context = {
        'first_name': request.user.first_name,
        'last_login': request.user.last_login,
    }
    return render(request, 'dashboard.html', context)

@login_required
def appointments(request):
    return render(request, 'appointments.html')

@login_required
def business_info(request):
    return render(request, 'business_info.html')

@login_required
def calendar_popup(request):
    return render(request, 'calendar_popup.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if new_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            logger.debug(f"Contraseña cambiada para el usuario {user.username}")
            return JsonResponse({'message': 'Contraseña cambiada exitosamente'})
        else:
            return JsonResponse({'error': 'Por favor ingresa una contraseña válida'}, status=400)
    
    return render(request, 'change_password.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        logger.debug(f"Perfil actualizado para el usuario {user.username}")
        return JsonResponse({'message': 'Perfil actualizado exitosamente'})
    else:
        return render(request, 'profile.html', {'user': request.user})

@login_required
def clients(request):
    return render(request, 'clients.html')

@login_required
def communications(request):
    return render(request, 'communications.html')

@login_required
def chatbot(request):
    return render(request, 'chatbot.html')

@login_required
def reports(request):
    return render(request, 'reports.html')

@login_required
def settings(request):
    return render(request, 'settings.html')

@login_required
def help(request):
    return render(request, 'help.html')

def chat_view(request):
    user_message = request.GET.get('message', '')
    bot_response = get_chat_response(user_message)  # Suponiendo que tienes una función para obtener la respuesta del chatbot
    return JsonResponse({'response': bot_response})
