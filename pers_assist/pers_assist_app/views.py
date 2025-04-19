from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ContactForm, ContactEditForm, NoteCreateForm, TagCreateForm, NoteEditForm
from .models import Contact, Note, Tag
from django.db.models import Q
from datetime import timedelta, date


def main(request):
    contacts = Contact.objects.all()
    return render(request, 'pers_assist_app/index.html', {
        'contacts': contacts,
    })


def contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': contacts,
    })


def contact_create(request):
    back_url = reverse('pers_assist_app:contacts')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/contact_create.html', {'form': form, 'back_url': back_url})

    return render(request, 'pers_assist_app/contact_create.html', {'form': ContactForm(), 'back_url': back_url})



def contact_detail(request, contact_id):
    back_url = reverse('pers_assist_app:contacts')
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'pers_assist_app/contact_detail.html', {"contact": contact, "back_url": back_url})


def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('pers_assist_app:contacts')

    return render(request, 'pers_assist_app/contact_confirm_delete.html', {"contact": contact})


def contact_edit(request, contact_id):
    back_url = reverse('pers_assist_app:contacts')

    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        form = ContactEditForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('pers_assist_app:contact_detail', contact_id=contact.id)
    else:
        form = ContactEditForm(instance=contact)

    return render(request, 'pers_assist_app/contact_edit.html', {'form': form, 'contact': contact, 'back_url': back_url})


def search_contacts(request):
    query = request.GET.get('search_item', '')
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query) |
            Q(surname__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        contacts = Contact.objects.all()

    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': contacts,
        'search_item': query,
    })


def search_birthdays(request):
    days_ahead = request.GET.get('days_ahead', 7)
    try:
        days_ahead = int(days_ahead)
    except ValueError:
        days_ahead = 7

    today = date.today()
    upcoming_dates = [(today + timedelta(days=i)) for i in range(days_ahead + 1)]
    upcoming_month_day = [(d.month, d.day) for d in upcoming_dates]

    contacts = Contact.objects.exclude(birthday=None)
    birthday_contacts = []

    for contact in contacts:
        if (contact.birthday.month, contact.birthday.day) in upcoming_month_day:
            birthday_contacts.append(contact)

    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': birthday_contacts,
        'days_ahead': days_ahead,
    })


# NOTES
def notes(requests, tag=None):
    if tag:
        tag_obj = get_object_or_404(Tag, slug__iexact=tag)
        all_notes = Note.objects.filter(tags=tag_obj)
    else:
        all_notes = Note.objects.all()

    all_tags = Tag.objects.all()

    return render(requests, 'pers_assist_app/notes.html', {'notes': all_notes, 'tags': all_tags})


def create_note(request):
    back_url = reverse('pers_assist_app:notes')

    if request.method == 'POST':
        form = NoteCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/note_create.html', {'form': form, 'back_url': back_url})

    return render(request, 'pers_assist_app/note_create.html', {'form': NoteCreateForm(), 'back_url': back_url})


def delete_note(request, note_id):
    all_notes = Note.objects.all()
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        note.delete()
        # print(f'{note.title} was deleted successful!')
        return redirect('pers_assist_app:notes')

    return render(request, 'pers_assist_app/notes.html', {'notes': all_notes})


def edit_note(request, note_id):
    back_url = reverse('pers_assist_app:notes')

    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('pers_assist_app:notes')
    else:
        form = NoteEditForm(instance=note)

    return render(request, 'pers_assist_app/note_edit.html', {'form': form, 'note': note, 'back_url': back_url})


def search_note_by_query(request):
    query = request.GET.get('q', '')
    all_notes = Note.objects.filter(text__icontains=query) or Note.objects.filter(title__icontains=query)

    all_tags = Tag.objects.all()

    return render(request, 'pers_assist_app/notes.html', {'notes': all_notes, 'tags': all_tags})




# TAGS
def create_tag(request):
    back_url = reverse('pers_assist_app:tag_create')

    if request.method == 'POST':
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/tag_create.html', {'form': form, 'back_url': back_url})

    return render(request, 'pers_assist_app/tag_create.html', {'form': TagCreateForm(), 'back_url': back_url})

