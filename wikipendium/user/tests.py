from django.test import TestCase
from django.contrib.auth.models import User
from wikipendium.user.forms import UserChangeForm


class UserTest(TestCase):

    def setUp(self):
        self.u1 = User(username='cristea')
        self.u2 = User(username='christoffer')
        self.u1.save()
        self.u2.save()

    def test_change_username(self):
        change_user_form = UserChangeForm({'username': 'christoffer'})
        self.assertFalse(change_user_form.is_valid())
