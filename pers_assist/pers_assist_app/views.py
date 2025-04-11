from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import Contact


# Create your views here.
def main(request):
    contacts = Contact.objects.all()
    return render(request, 'pers_assist_app/index.html', {"contacts": contacts})


def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='pers_assist_app:main')
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
        return redirect('pers_assist_app:main')
    return render(request, 'pers_assist_app/contact_confirm_delete.html', {"contact": contact})
