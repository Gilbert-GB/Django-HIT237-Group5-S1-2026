from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth import login
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            user = form.save()   # 👈 get the created user
            login(request, user) # 👈 auto login
            return redirect('dashboard')  # or 'home'

    return render(request, 'accounts/register.html', {'form': form})