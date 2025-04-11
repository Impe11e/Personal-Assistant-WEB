from django.forms import ModelForm, CharField, TextInput, DateInput, EmailField, DateField
from .models import Contact
from django import forms


class ContactForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput(attrs={'placeholder': 'John'}))
    surname = CharField(min_length=2, max_length=100, required=False, widget=TextInput(attrs={'placeholder': 'Johnson'}))
    address = CharField(max_length=150, required=False, widget=TextInput(attrs={'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'placeholder': '+380991234567'}))
    email = EmailField(required=False, widget=TextInput(attrs={'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=False, widget=DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    description = CharField(max_length=500, required=False, widget=TextInput(attrs={'placeholder': 'My old classmate'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']


class ContactEditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if self.instance and self.instance.id is not None:
            if self.instance.phone == phone:
                return phone

            if Contact.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
                raise forms.ValidationError('Contact with this phone number already exists')

        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].widget = DateInput(attrs={'type': 'date'})