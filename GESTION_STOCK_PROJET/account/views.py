from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Connection succes')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Donnees invalid')
            return redirect('login')
    else:
        return render(request, 'account/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

