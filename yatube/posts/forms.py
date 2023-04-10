from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        fields_required = ['text']
        labels = {'text': 'Текст поста',
                  'group': 'Группа'}
