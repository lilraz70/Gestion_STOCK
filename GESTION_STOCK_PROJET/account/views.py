from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Connection succes')
            return redirect('dashboard')
        else:
            messages.error(request, 'Donnees invalid')
            return redirect('login')
    else:
        return render(request, 'account/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Deconnection Reussi')
        return redirect('index')

