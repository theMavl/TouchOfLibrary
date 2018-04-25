from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required

from library.models import User, Document, Author, DocumentInstance, PatronType, Tag, \
    LibraryLocation, DocType, GiveOut
import datetime


@permission_required('library.add_document', 'library.add_user', 'library.add_patron')
def populate_db(request):
    perms_user = Permission.objects.filter(content_type=ContentType.objects.get(app_label="library", model="user"))
    perms_document = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="document"))
    perms_document_instance = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="documentinstance"))
    perms_reservation = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="reservation"))
    perms_giveout = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="giveout"))
    perms_tag = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="tag"))
    perms_doctype = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="doctype"))
    perms_document_request = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="documentrequest"))
    perms_author = Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="author"))
    perms_log= Permission.objects.filter(
        content_type=ContentType.objects.get(app_label="library", model="log"))

    libr_perms = [perms_document, perms_document_instance, perms_reservation, perms_giveout, perms_tag,
                  perms_doctype, perms_document_request, perms_author]

    admin_perms = [perms_user, perms_log]

    libr_1_perm = ["change_document", "change_documentinstance", "change_patron", "dashboard_access"]
    libr_2_perm = ["add_document", "add_documentinstance", "add_patron"]
    libr_3_perm = ["delete_document", "delete_documentinstance", "delete_patron", "put_outstanding", "delete_outstanding"]

    group_libr_1 = Group.objects.create(name='Librarian 1')
    group_libr_2 = Group.objects.create(name='Librarian 2')
    group_libr_3 = Group.objects.create(name='Librarian 3')
    group_libr = Group.objects.create(name='Super Librarian')
    group_admin = Group.objects.create(name='Administrator')

    for p in libr_perms:
        for perm in p:
            group_libr.permissions.add(perm)
            group_admin.permissions.add(perm)

    for p in admin_perms:
        for perm in p:
            group_admin.permissions.add(perm)

    perm_change_patron = Permission.objects.get(codename='change_patron')
    perm_add_patron = Permission.objects.get(codename='add_patron')
    group_libr.permissions.add(perm_change_patron)
    group_libr.permissions.add(perm_add_patron)

    for perm in libr_1_perm:
        group_libr_1.permissions.add(Permission.objects.get(codename=perm))
        group_libr_2.permissions.add(Permission.objects.get(codename=perm))
        group_libr_3.permissions.add(Permission.objects.get(codename=perm))

    for perm in libr_2_perm:
        group_libr_2.permissions.add(Permission.objects.get(codename=perm))
        group_libr_3.permissions.add(Permission.objects.get(codename=perm))

    for perm in libr_3_perm:
        group_libr_3.permissions.add(Permission.objects.get(codename=perm))

    type_student = PatronType.objects.create(title='Student', max_documents=5, max_renew_times=1, priority=50,
                                             position='n')
    type_faculty = PatronType.objects.create(title='Faculty member', max_documents=10, max_renew_times=1, priority=10,
                                             position='p')
    type_vp = PatronType.objects.create(title='Visiting Professor', max_documents=99999, max_renew_times=99999,
                                        priority=10,
                                        position='v')

    libradmin = User.objects.create_user(username='libradmin', email='libradmin@touchoflibrary.com',
                                         password='cakeisalie',
                                         first_name='John', last_name='Smith', phone_number='30000',
                                         address='Hidden', telegram='Hidden', is_patron=False)
    patr1 = User.objects.create_user(username='p1', email='first_patron@patronspace.com', password='cakeisalie',
                                     first_name='Sergey', last_name='Afonso', phone_number='30001',
                                     address='Via Margutta, 3', telegram='None',
                                     patron_type=type_faculty, is_patron=True)
    patr2 = User.objects.create_user(username='p2', email='second_patron@patronspace.com', password='cakeisalie',
                                     first_name='Nadia', last_name='Teixeira', phone_number='30002',
                                     address='Via Sacra, 13', telegram='None',
                                     patron_type=type_faculty, is_patron=True)
    patr3 = User.objects.create_user(username='p3', email='third_patron@patronspace.com', password='cakeisalie',
                                     first_name='Elvira', last_name='Espindola', phone_number='30003',
                                     address='Via del Corso, 22', telegram='None',
                                     patron_type=type_faculty, is_patron=True)
    prof = User.objects.create_user(username='prof', email='the_professor@patronspace.com', password='cakeisalie',
                                    first_name='Nickolay', last_name='Pink', phone_number='88005553535',
                                    address='Tatarstan, Innopolis city, st. Sportivnaya 2/3',
                                    telegram='@restorator',
                                    patron_type=type_faculty, is_patron=True)
    libr = User.objects.create_user(username='libr', email='libr@touch.com', password='cakeisalie',
                                    first_name='John',
                                    last_name='Smith')

    libr1 = User.objects.create_user(username='l1', email='libr1@touch.com', password='cakeisalie',
                                    first_name='Eugenia',
                                    last_name='Rama')
    libr2 = User.objects.create_user(username='l2', email='libr2@touch.com', password='cakeisalie',
                                     first_name='Luie',
                                     last_name='Ramos')
    libr3 = User.objects.create_user(username='l3', email='libr3@touch.com', password='cakeisalie',
                                     first_name='Ramon',
                                     last_name='Valdez')

    s = User.objects.create_user(username='s', email='student@touch.com', password='cakeisalie',
                                 first_name='Andrey',
                                 last_name='Velo', phone_number='30004',
                                 address='Avenida Mazatlan 250', telegram='@restorator',
                                 patron_type=type_student, is_patron=True)
    v = User.objects.create_user(username='v', email='vp@touch.com', password='cakeisalie', first_name='Veronika',
                                 last_name='Rama', phone_number='30005',
                                 address='Stret Atocha, 27', telegram='@restorator',
                                 patron_type=type_vp, is_patron=True)

    libr.groups.add(group_libr)
    libradmin.groups.add(group_admin)

    libr1.groups.add(group_libr_1)
    libr2.groups.add(group_libr_2)
    libr3.groups.add(group_libr_3)

    author1 = Author.objects.create(first_name='Thomas', last_name='Cormen')
    author2 = Author.objects.create(first_name='Charles', last_name='Leiserson', date_born='1953-10-10')
    author3 = Author.objects.create(first_name='Ronald', last_name='Rivest', date_born='1947-05-06')
    author4 = Author.objects.create(first_name='Clifford', last_name='Stein', date_born='1965-12-14')
    author5 = Author.objects.create(first_name='Niklaus', last_name='Wirth', date_born='1934-02-15')
    author6 = Author.objects.create(first_name='Donald', last_name='Knuth', date_born='1938-01-10')
    author7 = Author.objects.create(first_name='John', last_name='Vlissides')
    author8 = Author.objects.create(first_name='Richard', last_name='Helm')
    author9 = Author.objects.create(first_name='Brooks', last_name='Jr.')
    author10 = Author.objects.create(first_name='Frederick', last_name='P.')
    author11 = Author.objects.create(first_name='Tony', last_name='Hoare')
    author12 = Author.objects.create(first_name='Claude', last_name='Shannon')
    author12 = Author.objects.create(first_name='Claude', last_name='Shannon')

    tag1 = Tag.objects.create(caption='Algorithms')
    tag2 = Tag.objects.create(caption='Data Structures')
    tag3 = Tag.objects.create(caption='Complexity')
    tag4 = Tag.objects.create(caption='Computional Theory')
    tag5 = Tag.objects.create(caption='Search Algorithms')
    tag6 = Tag.objects.create(caption='Pascal')
    tag7 = Tag.objects.create(caption='Combinatorial Algorithms')
    tag8 = Tag.objects.create(caption='Recursion')

    type_book = DocType.objects.create(name='Book', fields='Publisher;Year;Edition', max_days=21,
                                       max_days_bestseller=14,
                                       max_days_privileges=28,
                                       max_days_visiting=7)

    # type_journal_article = DocType.objects.create(name='Journal article', fields='Issue;Publisher;Publication date',
    #                                             max_days=21, max_days_bestseller=14,
    #                                              max_days_privileges=28)

    type_av = DocType.objects.create(name='Audio/video material', fields='Director;Country;Year;Quality',
                                     max_days=14, max_days_bestseller=14,
                                     max_days_privileges=14,
                                     max_days_visiting=7)

    location1 = LibraryLocation.objects.create(room=401, level=2)
    location2 = LibraryLocation.objects.create(room=541, level=2)
    location3 = LibraryLocation.objects.create(room=221, level=3)

    doc1 = Document.objects.create(title='Introduction to Algorithms',
                                   description='The first edition won the award for Best 1990 Professional '
                                               'and Scholarly Book in Computer Science and Data Processing '
                                               'by the Association of American Publishers. There are books '
                                               'on algorithms that are rigorous but incomplete and others '
                                               'that cover masses of material but lack rigor. Introduction '
                                               'to Algorithms combines rigor and comprehensiveness.',
                                   type=type_book)
    doc1.authors.add(author1)
    doc1.authors.add(author2)
    doc1.authors.add(author3)
    doc1.authors.add(author4)
    doc1.tags.add(tag1)
    doc1.tags.add(tag2)
    doc1.tags.add(tag3)
    doc1.tags.add(tag4)
    doc11 = DocumentInstance.objects.create(document=doc1, status='a', location=location1, price=5000.0,
                                            additional_field1='MIT Press', additional_field2='2009',
                                            additional_field3='Third edition')
    doc12 = DocumentInstance.objects.create(document=doc1, status='a', location=location2, price=5000.0,
                                            additional_field1='MIT Press', additional_field2='2009',
                                            additional_field3='Third edition')
    doc13 = DocumentInstance.objects.create(document=doc1, status='a', location=location2, price=5000.0,
                                            additional_field1='MIT Press', additional_field2='2009',
                                            additional_field3='Third edition')

    doc2 = Document.objects.create(title='Algorithms + Data Structures = Programs',
                                   description="This is a classic book about basic algorithms and data structures. "
                                               "It's a must have book for understanding behind-the-scenes logic of "
                                               "standard libraries in modern programming languages. "
                                               "Should be on every programmer's read list.",
                                   type=type_book)
    doc2.authors.add(author5)
    doc2.tags.add(tag1)
    doc2.tags.add(tag2)
    doc2.tags.add(tag5)
    doc2.tags.add(tag6)

    doc21 = DocumentInstance.objects.create(document=doc2, status='a', location=location1, price=5000.0,
                                            additional_field1=' Prentice Hall PTR', additional_field2='1978',
                                            additional_field3='First edition')
    doc22 = DocumentInstance.objects.create(document=doc2, status='a', location=location1, price=5000.0,
                                            additional_field1=' Prentice Hall PTR', additional_field2='1978',
                                            additional_field3='First edition')
    doc23 = DocumentInstance.objects.create(document=doc2, status='a', location=location1, price=5000.0,
                                            additional_field1=' Prentice Hall PTR', additional_field2='1978',
                                            additional_field3='First edition')

    doc3 = Document.objects.create(title='The Art of Computer Programming',
                                   description='None',
                                   type=type_book)
    doc3.authors.add(author6)

    doc3.tags.add(tag7)
    doc3.tags.add(tag8)
    doc31 = DocumentInstance.objects.create(document=doc3, status='a', location=location2, price=5000.0,
                                            additional_field1='Addison-Wesley Longman Publishing Co., Inc.',
                                            additional_field2='1997', additional_field3='Third edition')
    doc32 = DocumentInstance.objects.create(document=doc3, status='a', location=location2, price=5000.0,
                                            additional_field1='Addison-Wesley Longman Publishing Co., Inc.',
                                            additional_field2='1997', additional_field3='Third edition')
    doc33 = DocumentInstance.objects.create(document=doc3, status='a', location=location2, price=5000.0,
                                            additional_field1='Addison-Wesley Longman Publishing Co., Inc.',
                                            additional_field2='1997', additional_field3='Third edition')

    doc4 = Document.objects.create(
        title='Null References: The Billion Dollar Mistake',
        description='Tony Hoare introduced Null references in ALGOL W back in 1965 "simply because it was so easy to implement", says Mr. Hoare. He talks about that decision considering it "my billion-dollar mistake".',
        type=type_av)
    doc4.authors.add(author11)
    doc4.tags.add(tag1)
    doc4.tags.add(tag4)

    doc41 = DocumentInstance.objects.create(document=doc4, status='a', location=location2, price=700.0,
                                            additional_field1='Spielberg',
                                            additional_field2='Agaganda', additional_field3='2013',
                                            additional_field4='Blue-Ray')
    doc42 = DocumentInstance.objects.create(document=doc4, status='a', location=location2, price=700.0,
                                            additional_field1='Spielberg',
                                            additional_field2='Agaganda', additional_field3='2013',
                                            additional_field4='DVD')

    doc5 = Document.objects.create(title='Information Entropy',
                                   description='None',
                                   type=type_av)
    doc5.authors.add(author12)
    doc5.tags.add(tag1)
    doc5.tags.add(tag4)

    DocumentInstance.objects.create(document=doc5, status='a', location=location2, price=3100.0,
                                    additional_field1='Spielberg',
                                    additional_field2='Agaganda', additional_field3='2013',
                                    additional_field4='Blue-Ray')
    DocumentInstance.objects.create(document=doc5, status='a', location=location2, price=1100.0,
                                    additional_field1='Spielberg',
                                    additional_field2='Agaganda', additional_field3='2013',
                                    additional_field4='DVD')

    # GIVE-OUTS

    # tt = datetime.datetime.strptime('26 Sep 2012', '%d %b %Y')
    # doc11.DEBUG_give_out(doc1, patr1, patr_info1, datetime.datetime.strptime('28 Mar 2018', '%d %b %Y'))

    # GiveOut.objects.filter(document_instance=doc11, patron=patr_info1).update(renewed_times=1)
    # doc11.due_back = datetime.datetime.strptime('31 Mar 2018', '%d %b %Y') + datetime.timedelta(doc1.days_available(patr_info1))

    # doc12.DEBUG_give_out(doc1, v, patr_infov, datetime.datetime.strptime('28 Mar 2018', '%d %b %Y'))

    # GiveOut.objects.filter(document_instance=doc12, patron=patr_infov).update(renewed_times=1)
    # doc12.due_back = datetime.datetime.strptime('31 Mar 2018', '%d %b %Y') + datetime.timedelta(doc1.days_available(patr_infov))

    return redirect('index')
