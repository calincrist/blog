from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish',
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     cleaned_data = super(PostForm, self).clean()
    #     return cleaned_data
