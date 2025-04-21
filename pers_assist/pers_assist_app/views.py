from django.http import Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ContactForm, ContactEditForm, NoteCreateForm, TagCreateForm, NoteEditForm, FileUploadForm
from .models import Contact, UploadedFile, Note, Tag
from datetime import timedelta, date
import cloudinary.uploader
import cloudinary
from django.contrib import messages  # если хочешь показать сообщения


@login_required(login_url='/signin/')
def main(request):
    contacts = Contact.objects.filter(owner=request.user)
    return render(request, 'pers_assist_app/index.html', {
        'contacts': contacts,
    })


@login_required(login_url='/signin/')
def contacts(request):
    contacts = Contact.objects.filter(owner=request.user)
    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': contacts,
    })


@login_required(login_url='/signin/')
def documents(request):
    category = request.GET.get('category')
    documents = UploadedFile.objects.filter(owner=request.user)

    if category:
        documents = documents.filter(category=category)

    context = {
        'documents': documents,
        'selected_category': category,
        'categories': dict(UploadedFile.CATEGORY_CHOICES)
    }

    return render(request, 'pers_assist_app/documents.html', context)


# CONTACTS
@login_required(login_url='/signin/')
def contact_create(request):
    back_url = reverse('pers_assist_app:contacts')

    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/contact_create.html', {'form': form, 'back_url': back_url})


    return render(request, 'pers_assist_app/contact_create.html', {'form': ContactForm(user=request.user), 'back_url': back_url})


@login_required(login_url='/signin/')
def contact_detail(request, contact_id):
    back_url = reverse('pers_assist_app:contacts')
    contact = get_object_or_404(Contact, pk=contact_id, owner=request.user)
    return render(request, 'pers_assist_app/contact_detail.html', {"contact": contact, "back_url": back_url})


@login_required(login_url='/signin/')
def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, owner=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('pers_assist_app:contacts')

    return render(request, 'pers_assist_app/contact_confirm_delete.html', {"contact": contact})


@login_required(login_url='/signin/')
def contact_edit(request, contact_id):
    back_url = reverse('pers_assist_app:contacts')
    contact = get_object_or_404(Contact, pk=contact_id, owner=request.user)
    
    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        print(f"Phone from POST: {request.POST.get('phone')}")
        
        form = ContactEditForm(request.POST, instance=contact, user=request.user)
        
        print(f"Raw phone from POST: {request.POST.get('phone')}")
        
        if form.is_valid():
            print(f"Form is valid, phone: {form.cleaned_data.get('phone')}")
            try:
                print(f"Validated phone: {form.cleaned_data.get('phone')}")
                
                contact = form.save(commit=False)
                contact.phone = form.cleaned_data['phone']
                print(f"Before save, phone: {contact.phone}")
                contact.save()
                return redirect('pers_assist_app:contact_detail', contact_id=contact.id)
            except Exception as e:
                print(f"Error saving form: {type(e)}: {str(e)}")
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = ContactEditForm(instance=contact, user=request.user)

    return render(request, 'pers_assist_app/contact_edit.html', {'form': form, 'contact': contact, 'back_url': back_url})
    

@login_required(login_url='/signin/')
def search_contacts(request):
    query = request.GET.get('search_item', '')
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query) |
            Q(surname__icontains=query) |
            Q(phone__icontains=query),
            owner=request.user
        )
    else:
        contacts = Contact.objects.filter(owner=request.user)

    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': contacts,
        'search_item': query,
    })


@login_required(login_url='/signin/')
def search_birthdays(request):
    days_ahead = request.GET.get('days_ahead', 7)
    try:
        days_ahead = int(days_ahead)
    except ValueError:
        days_ahead = 7

    today = date.today()
    upcoming_dates = [(today + timedelta(days=i)) for i in range(days_ahead + 1)]
    upcoming_month_day = [(d.month, d.day) for d in upcoming_dates]

    contacts = Contact.objects.exclude(birthday=None).filter(owner=request.user)
    birthday_contacts = []

    for contact in contacts:
        if (contact.birthday.month, contact.birthday.day) in upcoming_month_day:
            birthday_contacts.append(contact)

    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': birthday_contacts,
        'days_ahead': days_ahead,
    })


# NOTES
@login_required(login_url='/signin/')
def notes(requests, tag=None):
    if tag:
        tag_obj = get_object_or_404(Tag, slug__iexact=tag, owner=requests.user)
        all_notes = Note.objects.filter(tags=tag_obj, owner=requests.user)
    else:
        all_notes = Note.objects.filter(owner=requests.user)

    all_tags = Tag.objects.filter(owner=requests.user)

    return render(requests, 'pers_assist_app/notes.html', {'notes': all_notes, 'tags': all_tags})


@login_required(login_url='/signin/')
def create_note(request):
    back_url = reverse('pers_assist_app:notes')

    if request.method == 'POST':
        form = NoteCreateForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            form.save_m2m()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/note_create.html', {'form': form, 'back_url': back_url})

    return render(request, 'pers_assist_app/note_create.html', {
        'form': NoteCreateForm(user=request.user), 
        'back_url': back_url
    })

@login_required(login_url='/signin/')
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('pers_assist_app:notes')

    all_notes = Note.objects.filter(owner=request.user)
    return render(request, 'pers_assist_app/notes.html', {'notes': all_notes})


@login_required(login_url='/signin/')
def edit_note(request, note_id):
    back_url = reverse('pers_assist_app:notes')
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('pers_assist_app:notes')
    else:
        form = NoteEditForm(instance=note, user=request.user)

    return render(request, 'pers_assist_app/note_edit.html', {'form': form, 'note': note, 'back_url': back_url})

    
@login_required(login_url='/signin/')
def search_note_by_query(request):
    query = request.GET.get('q', '')
    all_notes = Note.objects.filter(
        Q(text__icontains=query) | Q(title__icontains=query),
        owner=request.user
    )

    all_tags = Tag.objects.filter(owner=request.user)

    return render(request, 'pers_assist_app/notes.html', {'notes': all_notes, 'tags': all_tags})


# TAGS
@login_required(login_url='/signin/')
def create_tag(request):
    back_url = reverse('pers_assist_app:note_create')

    if request.method == 'POST':
        form = TagCreateForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.owner = request.user
            tag.save()
            return redirect(back_url)
        else:
            return render(request, 'pers_assist_app/tag_create.html', {'form': form, 'back_url': back_url})

    return render(request, 'pers_assist_app/tag_create.html', {'form': TagCreateForm(), 'back_url': back_url})


# DOCUMENTS
@login_required(login_url='/signin/')
def upload_document(request):
    back_url = reverse('pers_assist_app:documents')

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            return redirect(back_url)
    else:
        form = FileUploadForm()

    return render(request, 'pers_assist_app/docs_upload.html', {'form': form, 'back_url': back_url})


@login_required(login_url='/signin/')
def document_download(request, document_id):
    try:
        document = get_object_or_404(UploadedFile, id=document_id, owner=request.user)
        if document.file:
            file_url = document.file.url
            return redirect(file_url)
        else:
            raise Http404("File not found")
    except UploadedFile.DoesNotExist:
        raise Http404("Document not found")


@login_required(login_url='/signin/')
def document_delete(request, document_id):
    back_url = reverse('pers_assist_app:documents')
    document = get_object_or_404(UploadedFile, pk=document_id, owner=request.user)

    if request.method == 'POST':
        try:
            cloudinary.uploader.destroy(document.file.public_id, invalidate=True)
        except Exception as e:
            print(f"An error occurred while deleting from Cloudinary: {e}")
        
        document.delete()
        return redirect('pers_assist_app:documents')

    return render(request, 'pers_assist_app/document_confirm_delete.html', {
        "document": document,
        "back_url": back_url
    })

    if request.method == 'POST':
        document.delete()
        return redirect('pers_assist_app:documents')

    return render(request, 'pers_assist_app/document_confirm_delete.html', {"document": document, "back_url": back_url})

