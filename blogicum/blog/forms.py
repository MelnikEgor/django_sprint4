from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Post, Comment, User
from blogicum.constants import (
    BAD_WORD,
    FORMAT_DATE_TIME,
    FROM_EMAIL,
    HEIGHT_COMMENT_FORM,
    WIDTH_COMMENT_FORM
)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'cols': WIDTH_COMMENT_FORM,
                    'rows': HEIGHT_COMMENT_FORM
                }
            )
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format=FORMAT_DATE_TIME,
                attrs={'type': 'datetime-local'}
            )
        }

    def clean(self):
        super().clean()
        text = self.cleaned_data['text']
        if BAD_WORD in f'{text.lower()}':
            send_mail(
                subject='Anton creat post',
                message=f'Имеются не цензурные выражения в тексте "{text}".'
                'Надо проверить!!!',
                from_email=FROM_EMAIL,
                recipient_list=['Admin@lst.net'],
                fail_silently=True,
            )
            raise ValidationError(
                'Выражайтесь пожалуйста культурно!!!'
            )
