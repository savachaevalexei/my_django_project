from django import forms
from .models import Category, Article, Comments
from captcha.fields import CaptchaField



class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории",
                                widget=forms.Select(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'cat',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AddCommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), initial=None)
    article = forms.CharField(widget=forms.HiddenInput(), initial=None)


    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.fields['article'].initial = self.instance.pk
        self.fields['parent_id'].initial = 0


    class Meta:
        model = Comments
        fields = ['comment', 'parent_id']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-comment'}),
        }

