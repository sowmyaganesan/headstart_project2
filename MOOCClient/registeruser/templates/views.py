from django.shortcuts import render


def search_form(request):
    return render(request, 'search_form.html')
