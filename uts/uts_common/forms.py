import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AzureDiamond'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hunter2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))


class TicketForm(forms.Form):
    owner = forms.ChoiceField(label="Crea come")
    name = forms.CharField(label="Titolo", widget=forms.TextInput())
    tags = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Lista di tag separati da una virgola (E.g. "amministrazione,studenti,segreteria")',
               'rows': 2}), required=False)

    def __init__(self, *args, user=None, **kwargs):
        if user is None:
            raise ValueError("TicketForm needs a user")
        super().__init__(*args, **kwargs)
        self.fields["owner"].choices = ((user.individual.id, user.full_name,),) + \
                                            tuple((org.id, org.name) for org in user.all_organizations)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Crea ticket'))

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["tags"] = [t.strip() for t in cleaned_data["tags"].split(",") if t.strip() != ""]
        if not any(re.match(r"^[\w\-\_\d\+]+$", tag) for tag in cleaned_data["tags"]):
            self.add_error("tags", "Tag non valido presente, caratteri speciali validi: -_+")

"""
            cleaned_data = super().clean()
            cc_myself = cleaned_data.get("cc_myself")
            subject = cleaned_data.get("subject")

            if cc_myself and subject and "help" not in subject:
                msg = "Must put 'help' in subject when cc'ing yourself."
                self.add_error('cc_myself', msg)
                self.add_error('subject', msg)
"""
