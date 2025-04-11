from django.shortcuts import render, redirect
from .forms import ContactForm


# Create your views here.
def main(request):
    return render(request, 'pers_assist_app/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='pers_assist_app:main')
        else:
            return render(request, 'pers_assist_app/contact.html', {'form': form})

    return render(request, 'pers_assist_app/contact.html', {'form': ContactForm()})
