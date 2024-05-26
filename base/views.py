from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout



# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('base/home.html')  
    else:
        form = AuthenticationForm()
    return render(request, 'base/login.html', {'form': form})


def home_view(request):
    return render(request, 'base/home.html')

