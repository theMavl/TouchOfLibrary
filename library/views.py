from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from library.forms import CheckOutButton
from .models import Document, Author, DocumentInstance, PatronInfo, Reservation, GiveOut, PatronType, Tag, \
    LibraryLocation, DocType
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import auth
import datetime
from django.contrib.auth.models import User, UserManager, Group, GroupManager, Permission
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType


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
    try:
        patron = PatronInfo.objects.get(user_id=user.id)
    except:
        patron = None
    reservation_list = Reservation.objects.filter(user_id=user.id)
    giveout_list = GiveOut.objects.filter(user_id=user.id)

    return render(
        request,
        'dashboard.html',
        context={'patron_user': user,
                 'patron_info': patron,
                 'reservation_table': reservation_list,
                 'giveout_table': giveout_list},
    )


@login_required
def patron_details(request, id):
    user = auth.get_user(request)

    if not user.has_perm('auth.change_user'):
        return redirect('dashboard')

    patron_user = User.objects.get(id=id)
    patron = PatronInfo.objects.get(user_id=patron_user.id)
    reservation_list = Reservation.objects.filter(user_id=patron_user.id)
    giveout_list = GiveOut.objects.filter(user_id=patron_user.id)

    return render(
        request,
        'library/patron_detail.html',
        context={'patron_user': patron_user,
                 'patron_info': patron,
                 'reservation_table': reservation_list,
                 'giveout_table': giveout_list},
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
    if not user.has_perm('auth.change_user'):
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


@permission_required('library.add_document', 'library.add_user', 'library.add_patroninfo')
def populate_db(request):
    perms_user = Permission.objects.filter(content_type=ContentType.objects.get(app_label="auth", model="user"))
    perms_document = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="document"))
    perms_document_instance = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="documentinstance"))
    perms_reservation = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="reservation"))
    perms_giveout = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="giveout"))

    libr_perms = [perms_user, perms_document, perms_document_instance, perms_reservation, perms_giveout]

    group_libr = Group.objects.create(name='Librarian')

    for p in libr_perms:
        for perm in p:
            group_libr.permissions.add(perm)

    patr1 = User.objects.create_user(username='patron1', email='first_patron@patronspace.com', password='cakeisalie',
                                     first_name='Anthony', last_name='Black')
    patr2 = User.objects.create_user(username='patron2', email='second_patron@patronspace.com', password='cakeisalie',
                                     first_name='Elon', last_name='Musk')
    prof = User.objects.create_user(username='prof', email='the_professor@patronspace.com', password='cakeisalie',
                                    first_name='Nickolay', last_name='Pink')
    libr = User.objects.create_user(username='libr', email='libr@touch.com', password='cakeisalie', first_name='John',
                                    last_name='Smith')

    libr.groups.add(group_libr)

    type_student = PatronType.objects.create(title='Student', max_documents=5, privileges=False)
    type_faculty = PatronType.objects.create(title='Faculty member', max_documents=10, privileges=True)

    PatronInfo.objects.create(user=patr1, phone_number='88005553535',
                              address='Tatarstan, Innopolis city, st. Sportivnaya 2/3', telegram='@restorator',
                              patron_type=type_student)
    PatronInfo.objects.create(user=patr2, phone_number='88005553535',
                              address='Tatarstan, Innopolis city, st. Sportivnaya 2/3', telegram='@restorator',
                              patron_type=type_student)
    PatronInfo.objects.create(user=prof, phone_number='88005553535',
                              address='Tatarstan, Innopolis city, st. Sportivnaya 2/3', telegram='@restorator',
                              patron_type=type_faculty)

    author1 = Author.objects.create(first_name='Bertran', last_name='Meyer')
    author2 = Author.objects.create(first_name='Thomas', last_name='Cormen')
    author3 = Author.objects.create(first_name='Jason', last_name='Smith')
    author5 = Author.objects.create(first_name='Alonso', last_name='Hitchkock')
    author6 = Author.objects.create(first_name='Officer', last_name='Black')
    author7 = Author.objects.create(first_name='Officer', last_name='Blue')

    tag1 = Tag.objects.create(caption='On English')
    tag2 = Tag.objects.create(caption='Programming')
    tag4 = Tag.objects.create(caption='Classic')
    tag5 = Tag.objects.create(caption='Hard reading')

    type_book = DocType.objects.create(name='Book', fields='Publisher;Year', max_days=21, max_days_bestseller=14,
                                       max_days_privileges=28)

    type_journal_article = DocType.objects.create(name='Journal article', fields='Issue;Publisher;Publication date',
                                                  max_days=21, max_days_bestseller=14,
                                                  max_days_privileges=28)

    type_av = DocType.objects.create(name='Audio/video material', fields='Director;Country;Year;Quality',
                                     max_days=14, max_days_bestseller=14,
                                     max_days_privileges=14)

    location1 = LibraryLocation.objects.create(room=401, level=2)
    location2 = LibraryLocation.objects.create(room=541, level=2)
    location3 = LibraryLocation.objects.create(room=221, level=3)

    doc1 = Document.objects.create(title='Touch of Class',
                                   description='Learn how to program well with objects and stuff', type=type_book)
    doc1.authors.add(author1)
    doc1.authors.add(author5)
    doc1.tags.add(tag1)
    doc1.tags.add(tag2)

    DocumentInstance.objects.create(document=doc1, status='a', location=location1, price=1200.0,
                                    additional_field1='The MIT Press', additional_field2='2018')
    DocumentInstance.objects.create(document=doc1, status='a', location=location2, price=200.0,
                                    additional_field1='The not MIT Press', additional_field2='1901')

    doc2 = Document.objects.create(title='Introduction to Algorithms',
                                   description='Dive in the world of painful sortings and other reason for khappy life',
                                   type=type_book)
    doc2.authors.add(author2)
    doc2.tags.add(tag1)
    doc2.tags.add(tag2)
    doc2.tags.add(tag5)

    DocumentInstance.objects.create(document=doc2, status='a', location=location3, price=2341.0,
                                    additional_field1='The MIT Press', additional_field2='2019')
    DocumentInstance.objects.create(document=doc2, status='a', location=location1, price=20220.0,
                                    additional_field1='The MIT Press', additional_field2='2020')

    doc3 = Document.objects.create(title='How to learn Eiffel',
                                   description='Find out whether it is even possible or not',
                                   type=type_journal_article)
    doc3.authors.add(author3)
    doc3.tags.add(tag1)
    doc3.tags.add(tag2)

    DocumentInstance.objects.create(document=doc3, status='a', location=location2, price=100.0,
                                    additional_field1='March 2018',
                                    additional_field2='Podval Press', additional_field3='7th March 2018')

    doc4 = Document.objects.create(title='Back to Uganda',
                                   description='DO YOU KNOW DE WEY',
                                   type=type_av)
    doc4.authors.add(author6)
    doc4.authors.add(author7)
    doc4.tags.add(tag1)
    doc4.tags.add(tag4)

    DocumentInstance.objects.create(document=doc4, status='a', location=location2, price=3100.0,
                                    additional_field1='Spielberg',
                                    additional_field2='Agaganda', additional_field3='2013',
                                    additional_field4='Blue-Ray')
    DocumentInstance.objects.create(document=doc4, status='a', location=location2, price=1100.0,
                                    additional_field1='Spielberg',
                                    additional_field2='Agaganda', additional_field3='2013',
                                    additional_field4='DVD')
    # Reservation.objects.create(user=user, document=document, document_copy=copy, executed=False).save()
    return redirect('index')


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
