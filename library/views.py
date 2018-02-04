from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
import datetime

from library.forms import OrderDocument
from .models import Document, Author, DocumentInstance, PatronInfo
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import auth
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist


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


# function that provides response with information.html file filled with content
# (with content from user and patronInfo models)
# working for an /information/ url request, (requires to be authorized)

@login_required
def account(request):
    user = auth.get_user(request)

    try:
        return render(
            request,
            'account.html',
            context={'user': user,
                     'FirstName': User.objects.get(id=user.id).first_name,
                     'LastName': User.objects.get(id=user.id).last_name,
                     'Email': User.objects.get(id=user.id).email,
                     'Address': PatronInfo.objects.get(user_id=user.id).address,
                     'Telegram': PatronInfo.objects.get(user_id=user.id).telegram,
                     'Phone_Number': PatronInfo.objects.get(user_id=user.id).phone_number},
        )
    except ObjectDoesNotExist:
        return render(
            request,
            'account.html',
            context={'user': user,
                     'FirstName': User.objects.get(id=user.id).first_name,
                     'LastName': User.objects.get(id=user.id).last_name,
                     'Email': User.objects.get(id=user.id).email,
                     'Address': "You have no Patron status",
                     'Telegram': "You have no Patron status",
                     'Phone_Number': "You have no Patron status"},
        )


class DocumentListView(generic.ListView):
    """
    page with all documents
    """
    model = Document
    paginate_by = 10


class AuthorsListView(generic.ListView):
    """
    page with all authors
    """
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """
    page with information about author
    """
    model = Author


def get_document_detail(request, id):
    """
    page with information about document and its copies
    """
    # List of all copies of current document
    copy_list = DocumentInstance.objects.filter(document_id=id)
    document = Document.objects.get(id=id)

    # html template
    return render(request, 'library/document_detail.html',
                  context={'copy_list': copy_list, "document": document})


def order_book(request, id):
    """
    page for ordering the document's copy
    """
    copy = get_object_or_404(DocumentInstance, pk=id)
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(14)

    # If POST request then process the input data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OrderDocument(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Change fields in data base table
            copy.due_back = form.cleaned_data["due_date"]
            copy.status = 'g'
            copy.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If  GET create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(14)
        form = OrderDocument(initial={"due_date": proposed_renewal_date, })

    # html template
    return render(request, 'library/order_details.html', {'form': form, 'copy': copy, 'date': proposed_renewal_date})
