from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, ListView
from django.db.models import Q

from account.models import UserProfile
from .forms import *


# Create your views here.

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'to_do_app/dashboard.html'
    paginate_by = 10
    context_object_name = 'tasks'
    login_url = reverse_lazy('account:login')

    def get_queryset(self):
        q = self.request.GET.get('q','')

        if q:
            return Task.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)) & Q(user__user=self.request.user)).order_by('-created_date')
        else:
            return Task.objects.filter(user__user=self.request.user).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class CreateTasksView(CreateView, LoginRequiredMixin):
    model = Task
    template_name = 'to_do_app/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('dashboard')
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        task = form.save(commit=False)
        task.user = user_profile
        task.save()
        return redirect('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateTasksView(UpdateView, LoginRequiredMixin):
    model = Task
    template_name = 'to_do_app/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('dashboard')
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        task = form.save(commit=False)
        task.user = user_profile
        task.save()
        return redirect('dashboard')

    def form_invalid(self, form):
        return redirect('dashboard')


class DeleteTasksView(DeleteView, LoginRequiredMixin):
    model = Task
    success_url = reverse_lazy('dashboard')
    login_url = reverse_lazy('account:login')


@login_required
def update_task_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=pk, user__user=request.user)

        task.status = not task.status
        task.save()

        if task.status:
            messages.success(request, f'✅ تسک "{task.title}" انجام شد!')
        else:
            messages.info(request, f'↩️ تسک "{task.title}" به لیست بازگشت!')

        return redirect('dashboard')
    else:
        return redirect('dashboard')
