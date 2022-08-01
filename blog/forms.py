from django import forms


class EmailPostForm(forms.Form):
    """
    Klasa formularza EmailPostForm.

    Pole typu CharField jest elementem typu <input type="text">
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
