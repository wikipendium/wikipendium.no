from django.forms import Form, CharField, ValidationError
from django.contrib.auth.models import User


class UserChangeForm(Form):
    username = CharField(max_length=30, label='New username')

    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()

        if User.objects.filter(username=cleaned_data['username']).count():
            raise ValidationError('Username already taken!')

        return cleaned_data
