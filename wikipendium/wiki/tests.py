"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from wikipendium.wiki.models import Article, ArticleContent, User
from django.core.exceptions import ValidationError
import datetime


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ArticleTest(TestCase):

    def setUp(self):
        self.u1 = User(username='u1')
        self.u2 = User(username='u2')
        self.u1.save()
        self.u2.save()
        self.article = Article(slug="TDT4100")
        self.article.save()
        self.ac1 = ArticleContent(article=self.article,
                                  updated=datetime.datetime(2012, 1, 1))
        self.ac2 = ArticleContent(article=self.article,
                                  updated=datetime.datetime(2013, 1, 1),
                                  title='per')
        self.ac1.edited_by = self.u1
        self.ac2.edited_by = self.u2
        self.ac1.save()
        self.ac2.save()

    def test_slug_should_uppercase_when_saved(self):
        article = Article()
        article.slug = "lowercase"
        article.save()
        self.assertEqual(article.slug, "LOWERCASE")

    def test_slug_cannot_contain_slashes(self):
        article = Article()
        article.slug = "TDT/4100"
        try:
            article.save()
            self.assertEqual(1, 2)  # this should not be reached
        except ValidationError:
            self.assertEqual(1, 1)  # correct error was raised

    def test_get_contributors(self):
        self.assertEquals(self.article.get_contributors(),
                          set([self.u1, self.u2]))

    def test_get_newest_content(self):
        self.assertEquals(self.article.get_newest_content(), self.ac2)

    def test_get_available_languages(self):
        self.assertEquals(self.article.get_available_languages(),
                          [('English', self.ac2)])

    def test_get_absolute_url(self):
        self.assertEquals(self.article.get_absolute_url(), "/TDT4100_per")
