from django.shortcuts import render, redirect
from library.models import Document, Author, DocumentInstance, PatronInfo


def index(request):
    """
    home page template
    """
    if request.user.is_authenticated:
        return redirect('document')
    else:
        return render(request, 'index.html')