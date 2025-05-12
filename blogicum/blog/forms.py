from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post, Comment, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea()
        }
        fields = '__all__'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        widgets = {
            'text': forms.Textarea()
        }
        fields = ('text',)


class UserFormMixin:
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


class BlogicumUserCreationForm(UserCreationForm):

    class Meta(UserFormMixin, UserCreationForm.Meta):
        pass


class BlogicumUserChangeForm(UserChangeForm):

    class Meta(UserFormMixin, UserChangeForm.Meta):
        pass
