from django.forms import ModelForm, CharField, TextInput, DateInput, EmailField, DateField, Textarea
from .models import Contact, UploadedFile, Note, Tag
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].widget = DateInput(attrs={'type': 'date'})

# NOTES
class NoteCreateForm(ModelForm):
    title = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'placeholder': 'Note'}))
    text = CharField(min_length=2, required=True, widget=Textarea(attrs={'placeholder': 'Note text'}))

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
        widget=forms.CheckboxSelectMultiple,  # или SelectMultiple, если хочешь dropdown
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']


class NoteEditForm(ModelForm):
    title = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'placeholder': 'Note'}))
    text = CharField(min_length=2, required=True, widget=Textarea(attrs={'placeholder': 'Note text'}))

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
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']


# TAGS
class TagCreateForm(ModelForm):
    tag_name = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'placeholder': '"New"'}))


    class Meta:
        model = Tag
        fields = ['tag_name']


# DOCUMENTS
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']
