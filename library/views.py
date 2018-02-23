from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from library.forms import CheckOutButton
from .models import Document, Author, DocumentInstance, PatronInfo, Reservation, GiveOut, PatronType
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import auth
import datetime
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required


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
def dashboard(request):
    user = auth.get_user(request)
    patron = PatronInfo.objects.get(user_id=user.id)
    reservation_list = list(Reservation.objects.filter(user_id=user.id))

    reservation_table = []
    giveout_table = []

    for reservation in reservation_list:
        reservation_table.append([reservation.document.title,
                                  reservation.document.type,
                                  reservation.document.quantity])

    users_books = list(DocumentInstance.objects.filter(holder=user.id))

    for books in users_books:
        string = ""
        for a in list(books.document.authors.all()):
            string += a.first_name + " " + a.last_name + "; "
        giveout_table.append([books.document.title,
                            string,
                            books.document.type.name,
                            books.due_back,
                            books.location])

    try:
        return render(
            request,
            'dashboard.html',
            context={
                'FirstName': user.first_name,
                'LastName': user.last_name,
                'Email': user.email,
                'Address': patron.address,
                'Telegram': patron.telegram,
                'Phone_Number': patron.phone_number,
                'reservation_table': reservation_table,
                'giveout_table': giveout_table},
        )
    except ObjectDoesNotExist:
        return render(
            request,
            'dashboard.html',
            context={'FirstName': user.first_name,
                     'LastName': user.last_name,
                     'Email': user.email,
                     'Address': "You have no Patron status",
                     'Telegram': "You have no Patron status",
                     'Phone_Number': "You have no Patron status",
                     'reservation_table': reservation_table,
                     'giveout_table': giveout_table},
        )


# @permission_required('library.change_patroninfo')
@login_required
def patron_details(request, id):
    user = auth.get_user(request)

    if not user.has_perm('library.change_patroninfo'):
        return redirect('dashboard')

    patron_user = User.objects.get(id=id)
    patron = PatronInfo.objects.get(user_id=patron_user.id)
    reservation_list = Reservation.objects.filter(user_id=patron_user.id)
    giveout_list = GiveOut.objects.filter(user_id=patron_user.id)

    try:
        return render(
            request,
            'library/patron_detail.html',
            context={'FirstName': patron_user.first_name,
                     'LastName': patron_user.last_name,
                     'Email': patron_user.email,
                     'Address': patron.address,
                     'Telegram': patron.telegram,
                     'Phone_Number': patron.phone_number,
                     'reservation_table': reservation_list,
                     'giveout_table': giveout_list},
        )
    except ObjectDoesNotExist:
        return render(
            request,
            'library/patron_detail.html',
            context={
                'FirstName': patron_user.first_name,
                'LastName': patron_user.last_name,
                'Email': patron_user.email,
                'Address': "No data",
                'Telegram': "No data",
                'Phone_Number': "No data",
                'reservation_table': reservation_list,
                'giveout_table': reservation_list},
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
    page with information about document
    """

    user = auth.get_user(request)
    document = Document.objects.get(id=id)
    additional = document.type.fields.split(sep=";")
    copy_list = DocumentInstance.objects.filter(document_id=id)

    if user.is_authenticated:
        reserved = Reservation.objects.filter(user_id=user.id, document_id=document.id)
        given_out = GiveOut.objects.filter(user=user, document=document)
        return render(request, 'library/document_detail.html',
                      context={'given_out': given_out,
                               'reserved': reserved,
                               "document": document,
                               "additional": additional,
                               "copy_list": copy_list})
    else:
        return render(request, 'library/document_detail.html',
                      context={"document": document, "additional": additional,
                               "copy_list": copy_list})


def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'library/reservation_list.html', context={'reservations': reservations})


def patrons_list(request):
    user = auth.get_user(request)
    if not user.has_perm('library.change_patroninfo'):
        return redirect('dashboard')

    record = PatronInfo.objects.all()
    return render(request, 'library/patrons_list.html', context={'patrons': record})


def giveout_list(request):
    giveouts = GiveOut.objects.all()
    return render(request, 'library/giveout_list.html', context={'giveouts': giveouts})


def giveout_confirmation(request, id):
    # TODO: Add custom date selector
    # TODO: Add more information about the reservation
    reservation = Reservation.objects.get(id=id)
    copy = reservation.document_copy
    patron = PatronInfo.objects.filter(user_id=reservation.user.id).first()
    patron_type = PatronType.objects.filter(id=patron.patron_type_id).first()
    if request.method == 'POST':
        form = CheckOutButton(request.POST)
        if form.clean_check_out():
            copy.document.quantity_synced = False
            copy.document.save()
            copy.status = 'g'
            copy.holder = reservation.user
            if patron_type.privileges:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days_privileges)
            elif copy.document.bestseller:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days_bestseller)
            else:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days)
            copy.save()

            GiveOut.objects.create(user=reservation.user, patron=patron, document=reservation.document,
                                   document_instance=copy)
            reservation.delete()
        return reservation_list(request)

    else:
        form = CheckOutButton()
        return render(request, 'library/giveout_details.html', context={'reservation': reservation, 'form': form})


def reserve_document(request, copy_id):
    user = auth.get_user(request)
    copy = DocumentInstance.objects.get(id=str(copy_id))
    document = Document.objects.get(id=copy.document_id)

    if user.is_authenticated:
        reserved = Reservation.objects.filter(user_id=user.id, document_copy_id=copy.id)
        checked_out = GiveOut.objects.filter(user=user, document=document)
        if reserved:
            reserved.delete()
            copy.status = "a"
        elif not checked_out and copy.status == "a" and not document.is_reference:
            Reservation.objects.create(user=user, document=document, document_copy=copy, executed=False).save()
            copy.status = "r"
        document.quantity_synced = False
        copy.save()
        document.save()
    return redirect('document-detail', id=document.id)


class DocumentCreate(CreateView):
    model = Document
    fields = '__all__'


class DocumentInstanceCreate(CreateView):
    model = DocumentInstance
    fields = '__all__'


class DocumentUpdate(UpdateView):
    model = Document
    fields = '__all__'
    template_name_suffix = '_update_form'
