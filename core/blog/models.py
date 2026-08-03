import uuid

from account.models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


# Create your models here.
class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ImageField(
        upload_to="blog/",
        default="blog/default.png",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="فقط فایل‌های تصویری با فرمت JPG, JPEG, PNG مجاز هستند.",
            )
        ],
        null=True,
        blank=True,
    )

    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:api-v1:post-detail",
            kwargs={
                "pk": self.pk,
                # "slug": self.slug,
            },
        )

    def get_snippet(self):
        return self.content[:50] + "..."


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]  # noqa: RUF012

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title[:30]}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CommentsReplies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_date"]  # noqa: RUF012

    def clean(self):
        if (hasattr(self, "author") and hasattr(self, "comment") and self.author and self.comment):
            # noqa: SIM102
            if self.author_id != self.comment.post.author_id:
                raise ValidationError("Only the post owner can reply to comments")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reply by {self.author} to {self.comment.author}"
