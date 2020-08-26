from django import forms
from bugs_app.models import MyUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["username", "password", "display_name"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)



# will also need new ticket form