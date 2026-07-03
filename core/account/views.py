
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .forms import *


# Create your views here.

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        return redirect('dashboard')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print('form valid')
        user = form.save()
        return redirect('login')

    def form_invalid(self, form):
        print(form.errors)
        return redirect('register')

@login_required
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')
    else:
        return redirect('dashboard')

