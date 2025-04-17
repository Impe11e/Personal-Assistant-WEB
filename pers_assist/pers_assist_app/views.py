from django.http import Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from .forms import ContactForm, ContactEditForm, FileUploadForm
from .models import Contact, UploadedFile

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


def documents(request):
    documents = UploadedFile.objects.all()
    return render(request, 'pers_assist_app/documents.html', {
        'documents': documents,
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
    upcoming_date = today + timedelta(days=days_ahead)

    upcoming_birthday_contacts = Contact.objects.filter(
        birthday__gte=today,
        birthday__lte=upcoming_date
    ).exclude(birthday=None)

    return render(request, 'pers_assist_app/contacts.html', {
        'contacts': upcoming_birthday_contacts,
        'days_ahead': days_ahead,
    })


def upload_document(request):
    back_url = reverse('pers_assist_app:documents')

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(back_url)
    else:
        form = FileUploadForm()

    return render(request, 'pers_assist_app/docs_upload.html', {'form': form, 'back_url': back_url})

# TODO: convert to cloud storage
def document_download(request, document_id):
    try:
        document = UploadedFile.objects.get(id=document_id)
        return FileResponse(document.file.open('rb'), as_attachment=True, filename=document.file.name)
    except UploadedFile.DoesNotExist:
        raise Http404("Document not found")

def document_delete(request, document_id):
    back_url = reverse('pers_assist_app:documents')
    document = get_object_or_404(UploadedFile, pk=document_id)
    if request.method == 'POST':
        document.delete()
        return redirect('pers_assist_app:documents')

    return render(request, 'pers_assist_app/document_confirm_delete.html', {"document": document, "back_url": back_url})


def search_documents(request):
    query = request.GET.get('search_item', '')
    if query:
        docuements = UploadedFile.objects.filter(title__icontains=query)
    else:
        docuements = UploadedFile.objects.all()

    return render(request, 'pers_assist_app/documents.html', {
        'documents': docuements,
        'search_item': query,
    })
