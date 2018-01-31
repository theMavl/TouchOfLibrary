from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Document, Author, DocumentInstance, PatronInfo
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    """
    home page template
    """
    # documents and their instances
    num_documents = Document.objects.all().count()
    num_instances = DocumentInstance.objects.all().count()

    num_authors = Author.objects.count()  # num of authors
    num_users = PatronInfo.objects.count

    # html template
    return render(
        request,
        'index.html',
        context={'num_documents': num_documents, 'num_instances': num_instances, 'num_authors': num_authors,
                 'num_users': num_users},
    )


@login_required
def information(request):
    user = auth.get_user(request)

    try:
        return render(
            request,
            'information.html',
            context={'user': user,
                     'Name': PatronInfo.objects.get(id=user.id).name,
                     'Address': PatronInfo.objects.get(id=user.id).address,
                     'Telegram': PatronInfo.objects.get(id=user.id).telegram,
                     'Phone_Number': PatronInfo.objects.get(id=user.id).phone_number},
        )
    except ObjectDoesNotExist:
        return render(
            request,
            'information.html',
            context={'user': user,
                     'Name': "You have no Patron status",
                     'Address': "You have no Patron status",
                     'Telegram': "You have no Patron status",
                     'Phone_Number': "You have no Patron status"},
        )


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
