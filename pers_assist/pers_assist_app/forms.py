from django.forms import ModelForm, CharField, TextInput, DateInput, EmailField, DateField, Textarea
from .models import Contact, Note, Tag
from django import forms


class ContactForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'John'}))
    surname = CharField(min_length=2, max_length=100, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Johnson'}))
    address = CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '+380991234567'}))
    email = EmailField(required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=False, widget=DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'DD-MM-YYYY'}))
    description = CharField(max_length=500, required=False, widget=Textarea(attrs={'class': 'input textarea-input', 'placeholder': 'My old classmate'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']


class ContactEditForm(forms.ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'John'}))
    surname = CharField(min_length=2, max_length=100, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Johnson'}))
    address = CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '+380991234567'}))
    email = EmailField(required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=False, widget=DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'DD-MM-YYYY'}))
    description = CharField(max_length=500, required=False, widget=Textarea(attrs={'class': 'input textarea-input', 'placeholder': 'My old classmate'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].widget = DateInput(attrs={'class': 'input', 'type': 'date'})


# NOTES
class NoteCreateForm(ModelForm):
    title = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Note'}))
    text = CharField(min_length=2, required=True, widget=Textarea(attrs={'class': 'input textarea-input', 'placeholder': 'Note text'}))

    color = forms.ChoiceField(
        choices=[
            ('red', 'Red'),
            ('green', 'Green'),
            ('blue', 'Blue'),
            ('purple', 'Purple'),
            ('yellow', 'Yellow'),

        ],
        widget=forms.Select(attrs={'class': 'input my-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'choice'}),  # или SelectMultiple, если хочешь dropdown
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']


class NoteEditForm(ModelForm):
    title = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Note'}))
    text = CharField(min_length=2, required=True, widget=Textarea(attrs={'class': 'input', 'placeholder': 'Note text'}))

    color = forms.ChoiceField(
        choices=[
            ('red', 'Red'),
            ('green', 'Green'),
            ('blue', 'Blue'),
            ('purple', 'Purple'),
            ('yellow', 'Yellow'),

        ],
        widget=forms.Select(attrs={'class': 'input my-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'choice'}),  # или SelectMultiple, если хочешь dropdown
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']


# TAGS
class TagCreateForm(ModelForm):
    tag_name = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '"New"'}))


    class Meta:
        model = Tag
        fields = ['tag_name']
