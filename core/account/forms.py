from django import forms
from django.contrib.auth import authenticate, password_validation
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
            attrs={"type": "date", "class": "form-control", "placeholder": "تاریخ تولد"}
        ),
        required=False,
        help_text="فرمت: YYYY-MM-DD",
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name:
            return first_name
        else:
            raise forms.ValidationError("Please enter a first name.")

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name:
            return last_name
        else:
            raise forms.ValidationError("Please enter a last name.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            check_dup = User.objects.filter(email__iexact=email)
            if check_dup.exists():
                raise forms.ValidationError("This email is already registered.")
            else:
                return email
        else:
            raise forms.ValidationError("Please enter a valid email.")

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date:
            return birth_date
        else:
            birth_date = None
            return birth_date

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) >= 8:
            return password1
        else:
            raise forms.ValidationError(
                "Please enter a password at least 8 characters."
            )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]

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
        fields = ("email", "password1", "password2")


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "required": True,
                "placeholder": "example@email.com",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"name": "password", "required": True, "placeholder": "********"}
        )
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password:
            return password
        else:
            raise forms.ValidationError("Please enter a password")

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError("email or password is incorrect.")
            elif not user.is_active:
                raise forms.ValidationError("Your account is disabled.")
            else:
                cleaned_data["user"] = user

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "birth_date")
        widgets = {  # noqa: RUF012
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "placeholder": "نام خود را وارد کنید",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "placeholder": "نام خانوادگی خود را وارد کنید",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "type": "date",
                }
            ),
        }


class PasswordEmailChangeForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل جدید",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                "placeholder": "example@email.com",
                "dir": "ltr",
            }
        ),
    )
    old_password = forms.CharField(
        label="رمز عبور فعلی",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                "placeholder": "رمز عبور فعلی",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                "placeholder": "رمز عبور جدید",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                "placeholder": "تکرار رمز عبور جدید",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["email"].initial = user.email

    def clean(self):
        cleaned_data = super().clean()

        email = (cleaned_data.get("email") or "").strip().lower()
        old_password = cleaned_data.get("old_password") or ""
        new_password1 = cleaned_data.get("new_password1") or ""
        new_password2 = cleaned_data.get("new_password2") or ""

        email_changed = bool(email) and email != self.user.email.lower()
        password_fields_filled = any([old_password, new_password1, new_password2])
        password_changed = bool(new_password1 or new_password2)

        if not email_changed and not password_fields_filled:
            raise forms.ValidationError(
                "حداقل ایمیل یا رمز عبور جدید را برای تغییر وارد کنید."
            )

        if not email_changed and password_fields_filled and not password_changed:
            self.add_error(
                "new_password1",
                "برای تغییر رمز، رمز عبور جدید را وارد کنید.",
            )

        if (
            email_changed and User.objects.exclude(pk=self.user.pk)
            .filter(email__iexact=email)
            .exists()
        ):
            self.add_error(
                "email",
                "این ایمیل قبلاً توسط کاربر دیگری ثبت شده است.",
            )

        if email_changed or password_changed:
            if not old_password:
                self.add_error(
                    "old_password",
                    "برای ذخیره تغییرات، رمز عبور فعلی را وارد کنید.",
                )
            elif not self.user.check_password(old_password):
                self.add_error(
                    "old_password",
                    "رمز عبور فعلی صحیح نیست.",
                )

        if password_changed:
            if not new_password1:
                self.add_error(
                    "new_password1",
                    "رمز عبور جدید را وارد کنید.",
                )

            if not new_password2:
                self.add_error(
                    "new_password2",
                    "تکرار رمز عبور جدید را وارد کنید.",
                )

            if new_password1 and new_password2:
                if new_password1 != new_password2:
                    self.add_error(
                        "new_password2",
                        "تکرار رمز عبور جدید با رمز عبور جدید یکسان نیست.",
                    )
                else:
                    try:
                        password_validation.validate_password(
                            new_password1,
                            self.user,
                        )
                    except forms.ValidationError as error:
                        self.add_error("new_password1", error)

        cleaned_data["email"] = email
        return cleaned_data

    def save(self):
        email = self.cleaned_data["email"]
        new_password = self.cleaned_data["new_password1"]

        if email and email != self.user.email.lower():
            self.user.email = email

        if new_password:
            self.user.set_password(new_password)

        self.user.save()
        return self.user
