from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "name": "first_name",
                "type": "text",
                "required": True,
                "placeholder": "first name",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "name": "last_name",
                "type": "text",
                "required": True,
                "placeholder": "first name",
            }
        )
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "تاریخ تولد"
            }
        ),
        required=False,
        help_text="فرمت: YYYY-MM-DD"
    )


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name
        else:
            raise forms.ValidationError('Please enter a first name.')

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name
        else:
            raise forms.ValidationError('Please enter a last name.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            check_dup = User.objects.filter(email__iexact=email)
            if check_dup.exists():
                raise forms.ValidationError('This email is already registered.')
            else:
                return email
        else:
            raise forms.ValidationError('Please enter a valid email.')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            return birth_date
        else:
            birth_date = None
            return birth_date

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) >= 8:
            return password1
        else:
            raise forms.ValidationError('Please enter a password at least 8 characters.')

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        birth_date = self.cleaned_data.get('birth_date')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                birth_date=self.cleaned_data["birth_date"],
            )

        return user

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "required": True,
                "placeholder": "example@email.com"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "name": "password",
                "required": True,
                "placeholder": "********"
            }
        )
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:
            return password
        else:
            raise forms.ValidationError('Please enter a password')

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:

            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError('email or password is incorrect.')
            elif not user.is_active:
                raise forms.ValidationError('Your account is disabled.')
            else:
                cleaned_data['user'] = user

        return cleaned_data
