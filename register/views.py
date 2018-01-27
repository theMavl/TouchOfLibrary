from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Document, Author, DocumentInstance, PatronInfo

def index(request):
    """
    home page template
    """
    # documents and their instances
    num_documents=Document.objects.all().count()
    num_instances=DocumentInstance.objects.all().count()

    num_authors=Author.objects.count()  # num of authors
    num_users = PatronInfo.objects.count

    # html template
    return render(
        request,
        'index.html',
        context={'num_documents':num_documents,'num_instances':num_instances,'num_authors':num_authors, 'num_users':num_users},
    )
from django.views import generic

class DocumentListView(generic.ListView):
    model = Document
    paginate_by = 10

class DocumentDetailView(generic.DetailView):
    model = Document

class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
