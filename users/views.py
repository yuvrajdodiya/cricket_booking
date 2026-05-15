from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import RegisterForm, LoginForm

# REGISTER VIEW
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # encrypt password
            user.save()
            return redirect('user_login')  # redirect after register
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


# LOGIN VIEW
def user_login_view(request):
    if request.user.is_authenticated:
             pass

    if request.method == 'POST':




        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                next_url = request.GET.get('next') or request.POST.get('next')
                return redirect(next_url or settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })
