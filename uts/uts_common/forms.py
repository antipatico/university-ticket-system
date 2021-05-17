import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div


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
    scheduled = forms.BooleanField(label="Invio Programmato", widget=forms.CheckboxInput(), required=False)
    scheduled_date = forms.DateField(label="Data", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    scheduled_time = forms.TimeField(label="Ora", widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    def __init__(self, *args, user=None, **kwargs):
        if user is None:
            raise ValueError("TicketForm needs a user")
        super().__init__(*args, **kwargs)
        self.fields["owner"].choices = ((user.individual.id, user.full_name,),) + \
                                            tuple((org.id, org.name) for org in user.all_organizations)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Crea ticket', css_class="col-12 mt-2"))
        self.helper.layout = Layout(
            Div(
                Field("owner"),
                Field("name"),
                Field("tags"),
                Div(
                    Div(Field("scheduled", v_model="scheduled"), css_class="col-md-6 col-sm-12"),
                    Div(Field("scheduled_date"), css_class="col-md-4 col-sm-12", v_if="scheduled"),
                    Div(Field("scheduled_time"), css_class="col-md-2 col-sm-12", v_if="scheduled"),
                    css_class="row", id="scheduleApp"
                ),
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["tags"] = [t.strip() for t in cleaned_data["tags"].split(",") if t.strip() != ""]
        if not any(re.match(r"^[\w\-\_\d\+]+$", tag) for tag in cleaned_data["tags"]):
            self.add_error("tags", "Tag non valido presente, caratteri speciali validi: -_+")
