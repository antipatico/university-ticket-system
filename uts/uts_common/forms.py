from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from uts_common.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AzureDiamond'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hunter2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))
