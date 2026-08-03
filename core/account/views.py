from blog.models import Posts
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormView

from account.models import UserProfile

from .forms import LoginForm, PasswordEmailChangeForm, ProfileEditForm, UserRegisterForm

# Create your views here.


class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("blog:blog_main")

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        return redirect("blog:blog_main")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return redirect("account:login")

    def form_invalid(self, form):
        return redirect("account:register")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard_base.html"
    login_url = reverse_lazy("account:login")


class PostListProfile(LoginRequiredMixin, ListView):
    model = Posts
    template_name = "account/my_posts.html"
    context_object_name = "posts"
    login_url = reverse_lazy("account:login")

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Posts.objects.filter(author=user_profile, status=True).annotate(
            new_comments_count=Count(
                "comments"
            )
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = "account/profile_edit.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("account:profile")


class PasswordEmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):

    form_class = PasswordEmailChangeForm
    template_name = "account/password_email_change.html"
    success_url = reverse_lazy("account:profile")
    success_message = "اطلاعات ورود شما با موفقیت به‌روزرسانی شد."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        password_changed = bool(form.cleaned_data["new_password1"])

        with transaction.atomic():
            user = form.save()

        if password_changed:
            update_session_auth_hash(self.request, user)

        return super().form_valid(form)


@login_required
def logout_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect("account:login")
    else:
        return redirect("ToDoApp:dashboard")
