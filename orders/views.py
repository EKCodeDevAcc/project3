from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'orders/index.html')
    return render(request, 'orders/login.html')

# Sign Up Page.
def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'orders/signUp.html', {'form': form})


# Login Page.
def loginPost(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'orders/login.html', {'message': 'Invalid credentials.'})


# Logout
def logoutPost(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})