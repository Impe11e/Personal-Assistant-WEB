from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelMultipleChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=75, required=True, widget=TextInput())
    born_date = DateField(required=False, widget=DateInput(attrs={"type": "date"}))
    born_location = CharField(min_length=3, max_length=25, required=False, widget=TextInput())
    description = CharField(min_length=3, required=False, widget=TextInput())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]

from django.forms import ModelChoiceField

class QuoteForm(ModelForm):
    quote = CharField(min_length=3, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']