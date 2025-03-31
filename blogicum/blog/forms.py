from django import forms
# Импортируем класс модели Birthday.
from .models import Post, Comment, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.TextInput()
        }
        fields = '__all__' 


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        widgets = {
            'text': forms.Textarea()
        }
        fields = ('text',)


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email') 