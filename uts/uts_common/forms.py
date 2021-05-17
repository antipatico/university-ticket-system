import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from django.utils import timezone
from uts_common.models import Profile
from django.utils.datetime_safe import datetime


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AzureDiamond'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hunter2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))


class ProfileSettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["email_notifications"]
        labels = {
            "email_notifications": "Notifiche via email"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salva'))



class TicketForm(forms.Form):
    owner = forms.ChoiceField(label="Crea come")
    name = forms.CharField(label="Titolo", widget=forms.TextInput())
    tags = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Lista di tag separati da una virgola (E.g. "amministrazione,studenti,segreteria")',
               'rows': 2}), required=False)
    scheduled = forms.BooleanField(label="Invio Programmato", widget=forms.CheckboxInput(), required=False)
    scheduled_date = forms.DateField(label="Data", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    scheduled_time = forms.TimeField(label="Ora", widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    scheduled_datetime = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, user=None, **kwargs):
        if user is None:
            raise ValueError("TicketForm needs a user")
        super().__init__(*args, **kwargs)
        self.fields["owner"].choices = ((user.individual.id, user.full_name,),) + \
                                       tuple((org.id, org.name) for org in user.all_organizations)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Crea ticket', css_class="col-12 mt-2", css_id="createTicket"))
        self.helper.layout = Layout(
            Div(
                Field("owner"),
                Field("name"),
                Field("tags"),
                Div(
                    Div(Field("scheduled", v_model="scheduled"), css_class="col-md-6 col-sm-12"),
                    Div(Field("scheduled_date", id="scheduleDate"), css_class="col-md-4 col-sm-12", v_if="scheduled"),
                    Div(Field("scheduled_time", id="scheduleTime"), css_class="col-md-2 col-sm-12", v_if="scheduled"),
                    css_class="row", id="scheduleApp"
                ),
                Field("scheduled_datetime", id="scheduleDateTime")
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["tags"] = [t.strip() for t in cleaned_data["tags"].split(",") if t.strip() != ""]
        if len(cleaned_data["tags"]) > 0 and not all(re.match(r"^[\w\-_\d+]+$", tag) for tag in cleaned_data["tags"]):
            self.add_error("tags", "Tag non valido presente, caratteri speciali validi: -_+")
        if cleaned_data["scheduled"]:
            if cleaned_data["scheduled_date"] is None:
                self.add_error("scheduled_date", "La data di invio programmato è necessaria")
            if cleaned_data["scheduled_time"] is None:
                self.add_error("scheduled_time", "L'orario di invio programmato è necessario")
            if cleaned_data["scheduled_datetime"] is None:
                self.add_error("scheduled", "Orario non valido")  # should never happen if js is good
            elif cleaned_data["scheduled_datetime"] < (timezone.now()+timezone.timedelta(minutes=5)):
                message = "Data troppo vicina (o forse nel passato!)"
                self.add_error("scheduled_date", message)
                self.add_error("scheduled_time", message)
