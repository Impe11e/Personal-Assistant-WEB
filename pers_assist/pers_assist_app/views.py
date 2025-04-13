from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, ContactEditForm
from .models import Contact
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='pers_assist_app:contacts')
        else:
            return render(request, 'pers_assist_app/contact_create.html', {'form': form})

    return render(request, 'pers_assist_app/contact_create.html', {'form': ContactForm()})


def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'pers_assist_app/contact_detail.html', {"contact": contact})


def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('pers_assist_app:contacts')

    return render(request, 'pers_assist_app/contact_confirm_delete.html', {"contact": contact})


def contact_edit(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        form = ContactEditForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('pers_assist_app:contact_detail', contact_id=contact.id)
    else:
        form = ContactEditForm(instance=contact)

    return render(request, 'pers_assist_app/contact_edit.html', {'form': form, 'contact': contact})


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
