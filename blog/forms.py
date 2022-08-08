from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """
    Klasa formularza EmailPostForm.

    Pole typu CharField jest elementem typu <input type="text">
    """
    name = forms.CharField(max_length=25, label='Imię')
    email = forms.EmailField(label='Email')
    to = forms.EmailField(label='Do')
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Treść')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
