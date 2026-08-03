from django import forms

from blog.models import Comments, CommentsReplies, Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content", "category", "image"]
        widgets = {  # noqa: RUF012
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition",
                    "placeholder": "یک عنوان جذاب انتخاب کنید...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition h-48 resize-none",
                    "placeholder": "محتوای مقاله را اینجا بنویسید...",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition bg-white",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "hidden",  # مخفی کردن برای استایل‌دهی با Alpine.js یا label سفارشی
                    "id": "post_image",
                    "accept": "image/*",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "content": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-800 "
                    "outline-none focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500",
                    "placeholder": "متن کامنت را اینجا بنویسید...",
                    "id": "comment_text",
                }
            )
        }


class ReplyForm(forms.ModelForm):
    comment_id = forms.UUIDField(widget=forms.HiddenInput())

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
                "class": "w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none bg-white shadow-sm transition",
                "placeholder": "پاسخ خود را به این کاربر بنویسید...",
            }
        ),
        error_messages={"required": "لطفاً متن پاسخ خود را وارد کنید."},
    )

    class Meta:
        model = CommentsReplies
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.instance.pk is None:
            self.fields["comment_id"].required = True
        else:
            self.fields["comment_id"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user

        if not instance.pk:
            instance.comment_id = self.cleaned_data["comment_id"]

        if commit:
            instance.save()
        return instance
