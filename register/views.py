from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse

from register.forms import OrderDocument
from .models import Document, Author, DocumentInstance, PatronInfo


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


from django.shortcuts import render


def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'register/user_profile.html', {"username": user})


import datetime


def get_document_detail(request, id):
    copy_list = DocumentInstance.objects.filter(document_id=id)
    document = Document.objects.get(id=id)
    date = (datetime.date.today() + datetime.timedelta(14)).__str__()

    return render(request, 'register/document_detail.html',
                  context={'copy_list': copy_list, "document": document, "date": date})


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime

@permission_required('catalog.can_mark_returned')
def order_book(request, id):
        """
        View function for renewing a specific BookInstance by librarian
        """
        copy = get_object_or_404(DocumentInstance, pk=id)
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(14)
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = OrderDocument(request.POST)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                copy.due_back = form.cleaned_data["due_date"]
                copy.status = 'g'
                copy.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('index'))

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(14)
            form = OrderDocument(initial={"due_date": proposed_renewal_date, })

        return render(request, 'register/order_details.html', {'form': form, 'copy': copy, 'date': proposed_renewal_date})

