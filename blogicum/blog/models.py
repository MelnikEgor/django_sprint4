from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .manager import PublishedPostManager
from blogicum.constants import LENGHT_STRING, MAX_QUANTITY_SYMBOLS
from core.models import DateTimeModel, PublishedModel


User = get_user_model()


class Category(DateTimeModel, PublishedModel):
    title = models.CharField(
        max_length=LENGHT_STRING,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    class Meta(DateTimeModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title} | {self.slug}'[:MAX_QUANTITY_SYMBOLS]


class Location(DateTimeModel, PublishedModel):
    name = models.CharField(
        max_length=LENGHT_STRING,
        verbose_name='Название места'
    )

    class Meta(DateTimeModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_QUANTITY_SYMBOLS]


class Post(DateTimeModel, PublishedModel):
    title = models.CharField(
        max_length=LENGHT_STRING,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    objects = models.Manager()
    published_post = PublishedPostManager()
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts_images',
        blank=True
    )

    class Meta(DateTimeModel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = (
            '-pub_date',
            'title',
        )

    def __str__(self):
        return self.title[:MAX_QUANTITY_SYMBOLS]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    @property
    def comment_count(self):
        return self.comments.count()


class Comments(models.Model):
    text = models.TextField(
        verbose_name='Комментарий'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
