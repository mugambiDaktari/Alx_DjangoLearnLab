from django import forms
from .models import Book
from django.core.validators import RegexValidator

class Form(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
        }



class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Only letters and spaces are allowed.')],
        strip=True
    )
    email = forms.EmailField(strip=True)
    age = forms.IntegerField(min_value=1, max_value=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_name(self):
        """Sanitize name field to prevent XSS attacks."""
        name = self.cleaned_data.get("name")
        if "<script>" in name:
            raise forms.ValidationError("Invalid input detected.")
        return name

    def clean_password(self):
        """Ensure password meets security requirements."""
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password