from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def register(request):
    #if request.user.is_authenticate:
    #    return redirect('/disclose/new_pet')
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        name = request.POST.get('nome')
        email = request.POST.get('email')
        passw = request.POST.get('senha')
        confirm_passw = request.POST.get('confirmar_senha')
        if len(name.strip()) == 0 or len(email.strip()) == 0 or len(passw.strip()) == 0 or len(confirm_passw.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, "register.html")
        if passw != confirm_passw:
            messages.add_message(request, constants.WARNING, 'Digite duas senhas iguais')
            return render(request, "register.html")
    try:
        user = User.objects.create_user(
            username=name,
            email=email,
            password=passw
        )
        messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
        return render(request, "register.html")
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return render(request, "register.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        name = request.POST.get("nome")
        passw = request.POST.get("senha")
        user = authenticate(username=name, password=passw)
        if len(name.strip()) == 0 or len(passw.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, "login.html")
        if user is not None:
            login(request, user)
            return redirect('/disclose/new_pet')
        messages.add_message(request, constants.ERROR, 'Credênciais invalidas')
        return render(request, "login.html")
def _logout(request):
    logout(request)
    return redirect('/auth/login')