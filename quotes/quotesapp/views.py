from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Tag, Quote
from .forms import TagForm, AuthorForm, QuoteForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})

@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)

            author_id = request.POST.get('author')
            try:
                author = Author.objects.get(id=author_id)
                new_quote.author = author
            except Author.DoesNotExist:
                return render(request, 'quotesapp/quote.html', {
                    "tags": tags,
                    "authors": authors,
                    "form": form,
                    "error": "Author does not exist"
                })

            new_quote.save()

            choice_tags = Tag.objects.filter(id__in=request.POST.getlist('tags'))
            new_quote.tags.set(choice_tags)

            return redirect('quotesapp:main')

        else:

            print("Form is not valid. Errors:", form.errors)

            return render(request, 'quotesapp/quote.html', {
                "tags": tags,
                "authors": authors,
                "form": form,
                "error": "Form is not valid. Please correct the errors below."
            })

    return render(request, 'quotesapp/quote.html', {
        "tags": tags,
        "authors": authors,
        "form": QuoteForm()
    })

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/author_detail.html', {"author": author})

