

from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ["full_name", "level"]

        labels = {
            "full_name": "نام و نام خانوادگی",
            "level": "سطح زبان فرانسه",
        }

        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "نام و نام خانوادگی خود را وارد کنید"
            }),
        }