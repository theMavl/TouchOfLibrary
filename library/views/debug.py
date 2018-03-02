from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required

from library.models import Document, Author, DocumentInstance, PatronInfo, PatronType, Tag, \
    LibraryLocation, DocType


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
