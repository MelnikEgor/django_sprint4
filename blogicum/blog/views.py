from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse

from .forms import CommentsForm, PostForm, UserForm
from .models import Category, Comments, Post, User
from blogicum.constants import COUNT_POSTS_PAGINATE


class CommetMixin:
    model = Comments
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = (self.object)
        return context

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class PaginateMixin:
    paginate_by = COUNT_POSTS_PAGINATE


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'


class ReverseMixin:
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class TemplateMixin:
    template_name = 'blog/create.html'


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentsForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = post
        comments.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(OnlyAuthorMixin, CommetMixin, UpdateView):
    form_class = CommentsForm


class CommentDeleteView(OnlyAuthorMixin, CommetMixin, DeleteView):
    pass


class ProfileView(PaginateMixin, PostMixin, ListView):
    template_name = 'blog/profile.html'

    def get_user(self):
        username = self.kwargs['username']
        return get_object_or_404(User, username=username)

    def get_queryset(self):
        user = self.get_user()
        if self.request.user == user:
            return user.posts.select_related(
                'author',
                'category',
                'location'
            ).prefetch_related(
                'comments'
            )
        else:
            return user.posts(
                manager='published_post'
            ).prefetch_related(
                'comments'
            )

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
    queryset = Post.published_post.all().prefetch_related(
        'comments'
    )


class PostCreateView(
    LoginRequiredMixin, ReverseMixin, TemplateMixin, CreateView
):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    OnlyAuthorMixin, PostMixin, TemplateMixin, UpdateView
):
    form_class = PostForm

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostDeleteView(
    OnlyAuthorMixin, PostMixin, ReverseMixin, TemplateMixin, DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        if self.request.user == post.author:
            return Post.objects.select_related(
                'author',
                'category',
                'location'
            ).filter(
                author=post.author
            ).prefetch_related(
                'comments'
            )
        else:
            return Post.published_post.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
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
            manager='published_post'
        ).all(
        ).prefetch_related(
            'comments'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context['category'] = category
        return context
