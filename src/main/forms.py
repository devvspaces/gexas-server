from django import forms
from django.core.validators import FileExtensionValidator


class FileForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['csv'])])

        