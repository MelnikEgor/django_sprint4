from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostQuerySet(models.query.QuerySet):

    def published_post(self):
        return self.select_related(
            'category',
            'author',
            'location',
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    def comment_count(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date',
            'title'
        )
