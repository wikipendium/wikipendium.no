from django.test import TestCase
from django.contrib.auth.models import User
from wikipendium.user.forms import UserChangeForm
from django.forms import ValidationError


class UserTest(TestCase):

    def setUp(self):
        self.u1 = User(username='cristea')
        self.u2 = User(username='christoffer')
        self.u1.save()
        self.u2.save()

    def test_change_username(self):
        change_user_form = UserChangeForm(instance=self.u1)
        change_user_form.username = 'christoffer'
        self.assertRaises(ValidationError,
                          UserChangeForm,
                          change_user_form.save())
