from django import forms
from bugs_app.models import MyUser, Ticket

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["username", "password", "display_name"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # choice = forms.ChoiceField(help_text='Status', choices=[(, 'Boast'), (False, 'Roast')])
        fields = ["title", "description"]

