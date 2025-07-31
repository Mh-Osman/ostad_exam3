from django import forms
from .models import Job, Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'description']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [('employer', 'Employer'), ('applicant', 'Applicant')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
