from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View

from django.contrib.auth import views as auth_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegistrationForm

class UserLoginView(auth_view.LoginView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form':form})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect(reverse('home:home'))
        else:
            return redirect('/')


class UserLogoutView(auth_view.LogoutView):
    def get(self, request):
        return render(request, 'home.html')


# Create your views here.
class UserRegistration(View):
    def get(self, request):
        user = request.user

        form = RegistrationForm()
        return render(request, 'registration.html', {'form' : form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            User.objects.create_user(username=username, password=password, email=email)
            return render(request, 'home.html')

        else:
            form = RegistrationForm()
            return redirect(reverse('register:user'), {'form' : form})
