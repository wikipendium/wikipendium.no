from django.forms import ModelForm, ValidationError
import django.forms as forms
from django.core.exceptions import ObjectDoesNotExist
from wikipendium.wiki.models import Article, ArticleContent
from wikipendium.wiki.merge3 import MergeError, merge
from wikipendium.wiki.langcodes import LANGUAGE_NAMES
from wikipendium.urls import slug_regex
from re import match


class ArticleForm(ModelForm):
    slug = forms.CharField(label='')
    language_list = sorted(LANGUAGE_NAMES.items(), key=lambda x: x[1])
    choices = [('', '')] + language_list
    lang = forms.ChoiceField(label='', choices=choices)
    title = forms.CharField(label='')
    content = forms.CharField(label='', widget=forms.Textarea())
    pk = forms.IntegerField(label='', widget=forms.HiddenInput())

    class Meta:
        model = ArticleContent
        fields = ('lang', 'title', 'content')

    def __init__(self, *args, **kwargs):
        if 'new_article' in kwargs:
            self.new_article = kwargs.pop('new_article')

        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['placeholder'] = 'Course code'
        self.fields['pk'].widget.attrs['value'] = 0
        self.fields['lang'].widget.attrs = {
            'class': "select_chosen",
            'data-placeholder': "Language"
        }

        try:
            if self.instance.article:
                slug = self.instance.article.slug
                self.fields['slug'].widget.attrs['value'] = slug
                if self.instance.article.pk:
                    self.fields['slug'].widget.attrs['readonly'] = True
                    existing_langs = (
                        self.instance.article.get_available_language_codes()
                    )
                    filtered_choices = [x
                                        for x
                                        in self.fields['lang'].choices
                                        if x[0] not in existing_langs]
                    self.fields['lang'].choices = filtered_choices
                if self.instance.pk:
                    self.fields['pk'].widget.attrs['value'] = self.instance.pk
                    self.fields['lang'].widget = forms.TextInput(attrs={
                        'readonly': True
                    })
        except:
            pass

        self.fields['title'].widget.attrs['placeholder'] = 'Course title'
        self.fields.keyOrder = ['pk', 'slug', 'lang', 'title', 'content']

    def clean(self):
        super(ArticleForm, self)
        if 'slug' in self.cleaned_data and 'lang' in self.cleaned_data:
            self.merge_contents_if_needed()
        return self.cleaned_data

    def clean_slug(self):
        if not match('^' + slug_regex + '$', self.cleaned_data['slug']):
            raise ValidationError('Course codes must be alphanumeric.')
        if self.new_article:
            try:
                Article.objects.get(slug=self.cleaned_data['slug'].upper())
                raise ValidationError("This course code is already in use")
            except ObjectDoesNotExist:
                pass
        return self.cleaned_data['slug']

    def merge_contents_if_needed(self):
        parentId = self.cleaned_data['pk']
        article = None
        articleContent = None
        slug = self.cleaned_data['slug']
        lang = self.cleaned_data['lang']
        try:
            article = Article.objects.get(slug=slug)
        except:
            article = Article(slug=slug)
        try:
            articleContent = article.get_newest_content(lang)
        except:
            articleContent = ArticleContent(article=article, lang=lang)

        if parentId and parentId != articleContent.pk:
            parent = ArticleContent.objects.get(id=parentId)
            a = parent
            b = articleContent
            ancestors = set()
            commonAncestor = None
            while True:
                if a.pk in ancestors:
                    commonAncestor = a
                    break
                if b.pk in ancestors:
                    commonAncestor = b
                    break
                ancestors.add(a.pk)
                ancestors.add(b.pk)
                a = a.parent
                b = b.parent
                if a.parent is None and b.parent is None:
                    break

            try:
                merged = merge(self.cleaned_data['content'],
                               commonAncestor.content, articleContent.content)
                self.cleaned_data['content'] = merged
            except MergeError as e:
                raise ValidationError("Merge conflict", params=e.diff)

        return True
