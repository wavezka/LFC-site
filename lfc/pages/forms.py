

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    hiddenimage = forms.CharField()



class Registrationform(UserCreationForm):
    email = forms.EmailField(required=True)

    hiddenimage = forms.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "hiddenimage",
        )

    def save(self, commit=True):
        user = super(Registrationform, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        UserProfile(user=user, username=self.cleaned_data['username'], head_shott=self.cleaned_data['hiddenimage']).save()
        return user
