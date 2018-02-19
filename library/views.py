from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
import datetime

from library.forms import ReserveButton, CheckOutButton
from .models import Document, Author, DocumentInstance, PatronInfo, WishList, RecordsLog, PatronType
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
def dashboard(request):
    user = auth.get_user(request)
    wish_list = list(WishList.objects.filter(user_id=user.id))

    wish_table = []
    book_table = []

    for wishes in wish_list:
        wish_table.append([wishes.document.title,
                           wishes.document.type,
                           wishes.document.quantity])

    users_books = list(DocumentInstance.objects.filter(holder=user.id))

    for books in users_books:
        string = ""
        for a in list(books.document.authors.all()):
            string += a.first_name + " " + a.last_name + "; "
        book_table.append([books.document.title,
                           string,
                           books.document.type.name,
                           books.due_back,
                           books.location])

    try:
        return render(
            request,
            'dashboard.html',
            context={'user': user,
                     'FirstName': User.objects.get(id=user.id).first_name,
                     'LastName': User.objects.get(id=user.id).last_name,
                     'Email': User.objects.get(id=user.id).email,
                     'Address': PatronInfo.objects.get(user_id=user.id).address,
                     'Telegram': PatronInfo.objects.get(user_id=user.id).telegram,
                     'Phone_Number': PatronInfo.objects.get(user_id=user.id).phone_number,
                     'wish_table': wish_table,
                     'book_table': book_table},
        )
    except ObjectDoesNotExist:
        return render(
            request,
            'dashboard.html',
            context={'user': user,
                     'FirstName': User.objects.get(id=user.id).first_name,
                     'LastName': User.objects.get(id=user.id).last_name,
                     'Email': User.objects.get(id=user.id).email,
                     'Address': "You have no Patron status",
                     'Telegram': "You have no Patron status",
                     'Phone_Number': "You have no Patron status",
                     'wish_table': wish_table,
                     'book_table': book_table},
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
        wished = WishList.objects.filter(user_id=user.id, document_id=document.id)
        ordered = RecordsLog.objects.filter(user=user, document=document)

        if request.method == 'POST':
            form = ReserveButton(request.POST)
            if form.clean_order():

                record = WishList.objects.create(user=user, document=document, executed=False)
                record.save()
                # if user.patrontype.privileges == 1:
                #   document.quantity = document.quantity-1
                #   document.save()
            else:
                WishList.objects.filter(user_id=user.id, document_id=document.id).delete()
                # if user.patrontype.privileges == 1:
                #    document.quantity = document.quantity + 1
                #    document.save()
                # TODO connect user with patrontype
            wished = WishList.objects.filter(user=user, document=document)
            ordered = RecordsLog.objects.filter(user_id=user.id, document_id=document.id)

        else:
            form = ReserveButton()
        # html template
        return render(request, 'library/document_detail.html',
                      context={'ordered': ordered,
                               'wished': wished,
                               "document": document,
                               "additional": additional,
                               "copy_list": copy_list})
    else:
        return render(request, 'library/document_detail.html',
                      context={"document": document})


def order_list(request):
    orders = WishList.objects.all()
    return render(request, 'library/order_list.html', context={'orders': orders})


def record_list(request):
    record = RecordsLog.objects.all()
    return render(request, 'library/record_list.html', context={'records': record})


def order_confirmation(request, id):
    order = WishList.objects.get(id=id)
    copies = DocumentInstance.objects.filter(document_id=order.document.id, status='a')
    patron = PatronInfo.objects.filter(user_id=order.user.id).first()
    patron_type = PatronType.objects.filter(id=patron.patron_type_id).first()
    copy = copies[0]
    if request.method == 'POST':
        form = CheckOutButton(request.POST)
        if form.clean_check_out():
            copy.document.quantity = copy.document.quantity - 1
            copy.document.save()
            copy.status = 'g'
            copy.holder = order.user
            # TODO connect user with patrontype
            if patron_type.privileges:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days_privileges)
            elif copy.document.bestseller:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days_bestseller)
            else:
                copy.due_back = datetime.date.today() + datetime.timedelta(copy.document.type.max_days)
            copy.save()
            order.delete()
            RecordsLog.objects.create(user=order.user, document=order.document, document_instance=copy,
                                      action=0, timestamp=copy.due_back)
        return order_list(request)

    else:
        form = CheckOutButton()
        return render(request, 'library/order_details.html', context={'order': order, 'form': form})
