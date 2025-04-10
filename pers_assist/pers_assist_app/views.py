from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'pers_assist_app/index.html')
