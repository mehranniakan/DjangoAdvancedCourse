# Create your views here.
from uuid import UUID

from account.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.filters import PostFilters
from blog.forms import CommentForm, PostForm, ReplyForm
from blog.models import Category, Comments, CommentsReplies, Posts


def active_user(user):
    return user.is_authenticated and user.is_active


class PostListView(ListView):
    template_name = "blog/main.html"
    filterset_class = PostFilters
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        self.categories = Category.objects.all()

        self.filterset_class = self.filterset_class(
            self.request.GET, queryset=Posts.objects.all()
        )
        return self.filterset_class.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        context["filter"] = self.filterset_class
        return context


class PostDetailView(DetailView):
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=...):
        if self.kwargs.get("id"):
            if UUID(str(self.kwargs.get("id"))):
                post_id = self.kwargs.get("id")

                post = get_object_or_404(
                    Posts.objects.select_related("author", "category"),
                    pk=post_id,
                    status=True,
                )

                return post

            else:
                raise Http404()
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        post_owner = False
        if self.request.user.is_authenticated:
            post_owner = Posts.objects.filter(
                pk=post.pk,
                author=UserProfile.objects.get(user=self.request.user),
            ).exists()

        context["is_post_owner"] = post_owner

        comments_qs = (
            Comments.objects.filter(post=post, is_approved=True)
            .select_related("author")
            .order_by("-created_date")
            .prefetch_related(
                Prefetch(
                    "commentsreplies_set",
                    queryset=CommentsReplies.objects.select_related("author").order_by(
                        "created_date"
                    ),
                )
            )
        )

        paginator = Paginator(comments_qs, 5)  # هر صفحه 5 کامنت
        page_number = self.request.GET.get("page")
        comments_page = paginator.get_page(page_number)
        context["reply_form"] = ReplyForm()
        context["comments_page"] = comments_page
        return context


@method_decorator(user_passes_test(active_user), name="dispatch")
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/add&edit_post.html"
    http_method_names = ["post", "get"]  # noqa: RUF012
    form_class = PostForm
    success_url = reverse_lazy("blog:blog_main")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = get_object_or_404(UserProfile, user=self.request.user)
        post.slug = f"{post.title}-{post.category.name}-{post.author.user.email}"
        post.save()
        messages.success(self.request, "پست شما با موفقیت ثبت شد")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(user_passes_test(active_user), name="dispatch")
class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "blog/add&edit_post.html"
    http_method_names = ["post", "get"]  # noqa: RUF012
    form_class = PostForm
    success_url = reverse_lazy("blog:blog_main")

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Posts.objects.filter(pk=post_id, author=user_profile)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = get_object_or_404(UserProfile, user=self.request.user)
        post.slug = f"{post.title}-{post.category.name}-{post.author.user.email}"
        post.save()
        messages.success(self.request, "پست شما با موفقیت ثبت شد")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(user_passes_test(active_user), name="dispatch")
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    success_url = reverse_lazy("blog:blog_main")

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Posts, pk=self.kwargs.get("pk"))
        post.delete()
        return redirect("blog:blog_main")


@method_decorator(user_passes_test(active_user), name="dispatch")
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm
    http_method_names = ["post"]  # noqa: RUF012
    success_url = reverse_lazy("blog_detail")

    def form_valid(self, form):
        post_id = self.request.POST.get("post_id")
        comment = form.cleaned_data["content"]

        post = get_object_or_404(Posts, pk=post_id)

        user_profile = UserProfile.objects.get(user=self.request.user)

        if Comments.objects.filter(author=user_profile, post=post).count() < 10:
            comment = Comments.objects.create(
                author=user_profile, content=comment, post=post
            )

            messages.success(self.request, "نظر شما با موفقیت ثبت شد.")
            return HttpResponseRedirect(self.get_success_url(post))

        else:
            messages.error(
                self.request, "شما به حداکثر تعداد مجاز کامنت (۱۰) رسیده‌اید."
            )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, post=None):
        if post:
            return reverse("blog:blog_detail", kwargs={"id": post.id})
        return reverse("blog:blog_main")

    def form_invalid(self, form):
        messages.error(self.request, "خطا در ثبت نظر. لطفاً دوباره تلاش کنید.")
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(user_passes_test(active_user), name="dispatch")
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    form_class = CommentForm
    template_name = "blog/edit_comment.html"

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Comments.objects.filter(author=user_profile).select_related("post")

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "نظر شما با موفقیت اصلاح شد.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"id": self.object.post_id})


@method_decorator(user_passes_test(active_user), name="dispatch")
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    http_method_names = ["post"]  # noqa: RUF012
    context_object_name = "comment"

    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("pk")

        if not comment_id:
            messages.error(request, "شناسه کامنت یافت نشد.")
            return redirect(self.get_success_url())

        try:
            UUID(str(comment_id))
        except ValueError:
            messages.error(request, "شناسه کامنت نامعتبر است.")
            return redirect(self.get_success_url())

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "پروفایل کاربر یافت نشد.")
            return redirect(self.get_success_url())

        comment = get_object_or_404(
            Comments.objects.filter(
                Q(author=user_profile) | Q(post__author=user_profile), id=comment_id
            )
        )

        post = comment.post

        comment.delete()
        messages.success(request, "نظر شما با موفقیت حذف شد.")

        return redirect(self.get_success_url(post))

    def get_success_url(self, post=None):
        if post:
            return reverse("blog:blog_detail", kwargs={"id": post.id})
        return reverse("blog:blog_main")


@method_decorator(user_passes_test(active_user), name="dispatch")
class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = CommentsReplies
    template_name = "blog/detail.html"
    form_class = ReplyForm
    http_method_names = ["post"]  # noqa: RUF012
    success_url = reverse_lazy("blog_detail")

    def form_valid(self, form):
        comment = Comments.objects.select_related("post").get(
            pk=form.cleaned_data["comment_id"]
        )
        author = UserProfile.objects.get(user=self.request.user)

        if CommentsReplies.objects.filter(comment=comment, author=author).count() < 10:
            self.object = form.save()

            messages.success(self.request, "پاسخ شما با موفقیت ثبت شد !")
            return redirect("blog:blog_detail", id=comment.post_id)

        else:
            messages.error(
                self.request, "حداکثر تعداد پاسخ مجاز برای یک کامنت 10 عدد می باشد"
            )
            return redirect("blog:blog_detail", id=comment.post_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_success_url(self, post=None):
        return reverse("blog:blog_detail", kwargs={"id": self.comment.post_id})


@method_decorator(user_passes_test(active_user), name="dispatch")
class ReplyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "blog/edit_reply.html"
    model = CommentsReplies
    form_class = ReplyForm
    success_url = reverse_lazy("blog_detail")

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return CommentsReplies.objects.select_related("comment__post").filter(
            pk=self.kwargs.get("pk"),
            author=user_profile,
        )

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "پاسخ شما با موفقیت ثبت شد !")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_success_url(self, post=None):
        return reverse("blog:blog_detail", kwargs={"id": self.object.comment.post_id})


@method_decorator(user_passes_test(active_user), name="dispatch")
class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = CommentsReplies
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        reply_id = self.kwargs.get("pk")

        if not reply_id:
            messages.error(request, "شناسه پاسخ یافت نشد.")
            return redirect(self.get_success_url())

        try:
            UUID(str(reply_id))
        except ValueError:
            messages.error(request, "شناسه پاسخ نامعتبر است.")
            return redirect(self.get_success_url())

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "پروفایل کاربر یافت نشد.")
            return redirect(self.get_success_url())

        reply = get_object_or_404(
            CommentsReplies.objects.filter(
                Q(author=user_profile) | Q(comment__post__author=user_profile),
                id=reply_id,
            )
        )

        post = reply.comment.post

        reply.delete()
        messages.success(request, "نظر شما با موفقیت حذف شد.")

        return redirect(self.get_success_url(post))

    def get_success_url(self, post=None):
        if post:
            return reverse("blog:blog_detail", kwargs={"id": post.id})
        return reverse("blog:blog_main")


@login_required
@user_passes_test(active_user)
def approve_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)

    if comment.post.author.user != request.user:
        messages.error(request, "شما دسترسی لازم برای تأیید این دیدگاه را ندارید.")
        return redirect("blog:blog_detail", id=comment.post.id)

    comment.is_approved = True
    comment.save()

    messages.success(request, "دیدگاه با موفقیت تأیید شد.")
    return redirect("blog:blog_detail", id=comment.post.id)
