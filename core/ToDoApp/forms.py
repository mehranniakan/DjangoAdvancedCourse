from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from ToDoApp.models import Task
from account.models import User, UserProfile


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        if self.instance:
            title = self.cleaned_data.get('title')
            if title:
                if self.instance.title == title:
                    return title
                else:
                    if Task.objects.filter(title__iexact=title, user__user=self.user, status=False).exists():
                        raise forms.ValidationError('You have already a open task with this title.')
                    else:
                        return title
            else:
                raise forms.ValidationError('Please enter a title for your task.')
        else:
            title = self.cleaned_data.get('title')
            if title:
                if Task.objects.filter(title=title).exists():
                    raise forms.ValidationError('One Task with this Title already registered.')
                else:
                    return title
            else:
                raise forms.ValidationError('Please enter a title for your task.')

    class Meta:
        model = Task
        fields = ['title', 'description']
