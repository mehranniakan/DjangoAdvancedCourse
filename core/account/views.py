from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from .forms import LoginForm, UserRegisterForm


# Create your views here.


class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("ToDoApp:dashboard")

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        return redirect("ToDoApp:dashboard")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return redirect("account:login")

    def form_invalid(self, form):
        return redirect("account:register")


@login_required
def logout_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect("account:login")
    else:
        return redirect("ToDoApp:dashboard")
