from django.forms import ModelForm, CharField, TextInput, DateInput, EmailField, DateField, Textarea
from .models import Contact, UploadedFile, Note, Tag
from django import forms


class ContactForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'John'}))
    surname = CharField(min_length=2, max_length=100, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Johnson'}))
    address = CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '+380991234567'}))
    email = EmailField(required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=False, widget=DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    description = CharField(max_length=500, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'My old classmate'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = self.user
        
        if user and phone:
            if Contact.objects.filter(owner=user, phone=phone).exists():
                raise forms.ValidationError("Contact with this phone number is already exists")
        
        return phone


class ContactEditForm(forms.ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'John'}))
    surname = CharField(min_length=2, max_length=100, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Johnson'}))
    address = CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Ukraine, Kyiv, Svobody av.'}))
    phone = CharField(max_length=20, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '+380991234567'}))
    email = EmailField(required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'exapmle@gmail.com'}))
    birthday = DateField(required=False, widget=DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    description = CharField(max_length=500, required=False, widget=TextInput(attrs={'class': 'input', 'placeholder': 'My old classmate'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'address', 'phone', 'email', 'birthday', 'description']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContactEditForm, self).__init__(*args, **kwargs)
        self.instance_id = self.instance.id if self.instance and self.instance.id else None

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = self.user
        
        if user and phone:
            existing_contacts = Contact.objects.filter(owner=user, phone=phone)
            
            if self.instance_id:
                existing_contacts = existing_contacts.exclude(id=self.instance_id)
                
            if existing_contacts.exists():
                raise forms.ValidationError("Contact with this phone number is already exists.")
        


# NOTES
class NoteCreateForm(ModelForm):
    title = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': 'Note'}))
    text = CharField(min_length=2, required=True, widget=Textarea(attrs={'class': 'input  textarea-input', 'placeholder': 'Note text'}))

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
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'choice my-select'}),
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['tags'].queryset = Tag.objects.filter(owner=self.user)



class NoteEditForm(ModelForm):
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
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'choice my-select'}),
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'color', 'tags']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['tags'].queryset = Tag.objects.filter(owner=self.user)


# TAGS
class TagCreateForm(ModelForm):
    tag_name = CharField(min_length=2, max_length=100, required=True, widget=TextInput(attrs={'class': 'input', 'placeholder': '"New"'}))


    class Meta:
        model = Tag
        fields = ['tag_name']


# DOCUMENTS
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']
