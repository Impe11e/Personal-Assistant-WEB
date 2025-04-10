from django.forms import ModelForm, CharField, TextInput, DateInput, EmailField, DateField
from .models import Contact


class ContactForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput(attrs={'placeholder': 'Lohn Doe'}))
    address = CharField(max_length=150, required=True, widget=TextInput(attrs={'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'placeholder': '+380991234567'}))
    email = EmailField(required=True, widget=TextInput(attrs={'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=True, widget=DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone', 'email', 'birthday']