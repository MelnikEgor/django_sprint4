from django.db import models
from django.db.models import Count
from django.utils import timezone


class PublishedPostManager(models.Manager):
    """
    Собственный менеджер.

    Фильтрация запросов на посты, которые опубликованы.
    Получение всех необходимых данныйх.
    """

    def get_queryset(self):
        return super().get_queryset().select_related(
            'category',
            'author',
            'location'
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )


class CountCommentsUnderPostManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date',
            'title'
        )
