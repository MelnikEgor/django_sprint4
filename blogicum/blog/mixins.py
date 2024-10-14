from django.urls import reverse

from .models import Comment, Post
from blogicum.constants import COUNT_POSTS_PAGINATE


class CommetMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

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
