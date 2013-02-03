from django.forms import ModelForm
import django.forms as forms
from wikipendium.wiki.models import Article, ArticleContent

class ArticleForm(ModelForm):
    slug = forms.CharField(label='')
    title = forms.CharField(label='')
    content = forms.CharField(label='',widget=forms.Textarea())

    class Meta:
        model = ArticleContent
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['placeholder'] = 'Course code'
        try:
            if self.instance.article:
                self.fields['slug'].widget.attrs['value'] = self.instance.article.slug
                if self.instance.article.pk:
                    self.fields['slug'].widget.attrs['readonly'] = True
        except:
            pass

        self.fields['title'].widget.attrs['placeholder'] = 'Course title'
        self.fields.keyOrder = ['slug','title','content']


