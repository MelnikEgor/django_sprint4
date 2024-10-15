from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm, UserForm
from .mixins import (
    CommetMixin,
    OnlyAuthorMixin,
    PaginateMixin,
    PostMixin,
    ReverseMixin,
    TemplateMixin
)
from .models import Category, Post, User


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = post
        comments.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    CommetMixin,
    UpdateView
):
    form_class = CommentForm


class CommentDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    CommetMixin,
    DeleteView
):
    pass


class ProfileView(PaginateMixin, PostMixin, ListView):
    template_name = 'blog/profile.html'

    def get_user(self):
        username = self.kwargs['username']
        return get_object_or_404(User, username=username)

    def get_queryset(self):
        user = self.get_user()
        if self.request.user == user:
            return user.posts(manager='custom_objects').comment_count(
            ).select_related(
                'category',
                'location',
                'author'
            )
        else:
            return user.posts(
                manager=('custom_objects')
            ).comment_count().published_post()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()
        context['profile'] = user
        return context


class UserUpdateView(LoginRequiredMixin, ReverseMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user


class PostListView(PaginateMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.custom_objects.comment_count().published_post()


class PostCreateView(
    LoginRequiredMixin, ReverseMixin, TemplateMixin, CreateView
):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, OnlyAuthorMixin, PostMixin, TemplateMixin, UpdateView
):
    form_class = PostForm

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    PostMixin,
    ReverseMixin,
    TemplateMixin,
    DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        post = get_object_or_404(
            Post.objects.select_related(
                'author',
                'category',
                'location',
            ),
            pk=self.kwargs['post_id']
        )
        if self.request.user != post.author:
            return get_object_or_404(
                Post.custom_objects.published_post(),
                pk=self.kwargs['post_id']
            )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CatgoryView(PaginateMixin, ListView):
    model = Category
    template_name = 'blog/category.html'

    def get_category(self):
        category = self.kwargs['category_slug']
        return get_object_or_404(
            Category.objects.filter(
                is_published=True
            ),
            slug=category
        )

    def get_queryset(self):
        category = self.get_category()
        return category.posts(
            manager='custom_objects'
        ).comment_count().published_post()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context['category'] = category
        return context
