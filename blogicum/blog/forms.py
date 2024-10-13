from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

from .models import Post, Comments, User
from blogicum.constants import BAD_WORD


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
        )
        fields = ('__all__')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        super().clean()
        text = self.cleaned_data['text']
        if BAD_WORD in f'{text.lower()}':
            send_mail(
                subject='Anton creat post',
                message=f'Имеются не цензурные выражения в тексте "{text}".'
                'Надо проверить!!!',
                from_email='post_form@lst.net',
                recipient_list=['Admin@lst.net'],
                fail_silently=True,
            )
            raise ValidationError(
                'Выражайтесь пожалуйста культурно!!!'
            )
