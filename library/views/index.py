from django.shortcuts import render
from library.models import Document, Author, DocumentInstance, PatronInfo


def index(request):
    """
    home page template
    """
    # num of documents and their instances
    num_documents = Document.objects.all().count()
    num_instances = DocumentInstance.objects.all().count()

    # num of authors
    num_authors = Author.objects.count()
    # num of users
    num_users = PatronInfo.objects.count

    # html template
    return render(
        request,
        'index.html',
        context={'num_documents': num_documents, 'num_instances': num_instances, 'num_authors': num_authors,
                 'num_users': num_users},
    )