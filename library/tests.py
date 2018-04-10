from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required

from library.models import Document, Author, DocumentInstance, PatronInfo, PatronType, Tag, \
    LibraryLocation, DocType, GiveOut


class Tests(TestCase):
    def setUp(self):
        perms_user = Permission.objects.filter(content_type=ContentType.objects.get(app_label="auth", model="user"))
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
        perms_patroninfo = Permission.objects.filter(
            content_type=ContentType.objects.get(app_label="library", model="patroninfo"))
        perms_document_request = Permission.objects.filter(
            content_type=ContentType.objects.get(app_label="library", model="documentrequest"))

        libr_perms = [perms_user, perms_document, perms_document_instance, perms_reservation, perms_giveout, perms_tag,
                      perms_doctype, perms_patroninfo, perms_document_request]

        group_libr = Group.objects.create(name='Librarian')

        for p in libr_perms:
            for perm in p:
                group_libr.permissions.add(perm)

        patr1 = User.objects.create_user(username='p1', email='first_patron@patronspace.com', password='cakeisalie',
                                         first_name='Sergey', last_name='Afonso')
        patr2 = User.objects.create_user(username='p2', email='second_patron@patronspace.com', password='cakeisalie',
                                         first_name='Nadia', last_name='Teixeira')
        patr3 = User.objects.create_user(username='p3', email='third_patron@patronspace.com', password='cakeisalie',
                                         first_name='Elvira', last_name='Espindola')
        prof = User.objects.create_user(username='prof', email='the_professor@patronspace.com', password='cakeisalie',
                                        first_name='Nickolay', last_name='Pink')
        libr = User.objects.create_user(username='libr', email='libr@touch.com', password='cakeisalie',
                                        first_name='John',
                                        last_name='Smith')
        s = User.objects.create_user(username='s', email='student@touch.com', password='cakeisalie',
                                     first_name='Andrey',
                                     last_name='Velo')
        v = User.objects.create_user(username='v', email='vp@touch.com', password='cakeisalie', first_name='Veronika',
                                     last_name='Rama')

        libr.groups.add(group_libr)

        type_student = PatronType.objects.create(title='Student', max_documents=5, max_renew_times=1, priority=50,
                                                 position='n')
        type_faculty = PatronType.objects.create(title='Faculty member', max_documents=10, max_renew_times=1,
                                                 priority=10,
                                                 position='p')
        type_vp = PatronType.objects.create(title='Visiting Professor', max_documents=99999, max_renew_times=99999,
                                            priority=10,
                                            position='v')

        patr_info1 = PatronInfo.objects.create(user=patr1, phone_number='30001',
                                               address='Via Margutta, 3', telegram='None',
                                               patron_type=type_faculty)
        patr_info2 = PatronInfo.objects.create(user=patr2, phone_number='30002',
                                               address='Via Sacra, 13', telegram='None',
                                               patron_type=type_faculty)
        patr_info3 = PatronInfo.objects.create(user=patr3, phone_number='30003',
                                               address='Via del Corso, 22', telegram='None',
                                               patron_type=type_faculty)
        patr_infop = PatronInfo.objects.create(user=prof, phone_number='88005553535',
                                               address='Tatarstan, Innopolis city, st. Sportivnaya 2/3',
                                               telegram='@restorator',
                                               patron_type=type_faculty)
        patr_infos = PatronInfo.objects.create(user=s, phone_number='30004',
                                               address='Avenida Mazatlan 250', telegram='@restorator',
                                               patron_type=type_student)
        patr_infov = PatronInfo.objects.create(user=v, phone_number='30005',
                                               address='Stret Atocha, 27', telegram='@restorator',
                                               patron_type=type_vp)

        author1 = Author.objects.create(first_name='Thomas', last_name='Cormen')
        author2 = Author.objects.create(first_name='Charles', last_name='Leiserson')
        author3 = Author.objects.create(first_name='Ronald', last_name='Rivest')
        author4 = Author.objects.create(first_name='Clifford', last_name='Stein')
        author5 = Author.objects.create(first_name='Erich', last_name='Gamma')
        author6 = Author.objects.create(first_name='Ralph', last_name='Johnson')
        author7 = Author.objects.create(first_name='John', last_name='Vlissides')
        author8 = Author.objects.create(first_name='Richard', last_name='Helm')
        author9 = Author.objects.create(first_name='Brooks', last_name='Jr.')
        author10 = Author.objects.create(first_name='Frederick', last_name='P.')
        author11 = Author.objects.create(first_name='Tony', last_name='Hoare')
        author12 = Author.objects.create(first_name='Claude', last_name='Shannon')

        tag1 = Tag.objects.create(caption='On English')
        tag2 = Tag.objects.create(caption='Programming')
        tag4 = Tag.objects.create(caption='Classic')
        tag5 = Tag.objects.create(caption='Hard reading')

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
        doc11 = DocumentInstance.objects.create(document=doc1, status='a', location=location1, price=5000.0,
                                                additional_field1='MIT Press', additional_field2='2009',
                                                additional_field3='Third edition')
        doc12 = DocumentInstance.objects.create(document=doc1, status='a', location=location2, price=5000.0,
                                                additional_field1='MIT Press', additional_field2='2009',
                                                additional_field3='Third edition')
        doc13 = DocumentInstance.objects.create(document=doc1, status='a', location=location2, price=5000.0,
                                                additional_field1='MIT Press', additional_field2='2009',
                                                additional_field3='Third edition')

        doc2 = Document.objects.create(title='Design Patterns: Elements of Reusable Object-Oriented Software',
                                       description='* Capturing a wealth of experience about the design of object-oriented software, four top-notch designers present a catalog of simple and succinct solutions to commonly occurring design problems. Previously undocumented, these 23 patterns allow designers to create more flexible, elegant, and ultimately reusable designs without having to rediscover the design solutions themselves. * The authors begin by describing what patterns are and how they can help you design object-oriented software. They then go on to systematically name, explain, evaluate, and catalog recurring designs in object-oriented systems. With Design Patterns as your guide, you will learn how these important patterns fit into the software development process, and how you can leverage them to solve your own design problems most efficiently.',
                                       type=type_book, bestseller=True)
        doc2.authors.add(author5)
        doc2.authors.add(author6)
        doc2.authors.add(author7)
        doc2.authors.add(author8)
        doc2.tags.add(tag1)
        doc2.tags.add(tag2)

        doc21 = DocumentInstance.objects.create(document=doc2, status='a', location=location3, price=1700.0,
                                                additional_field1='Addison-Wesley Professional',
                                                additional_field2='2003',
                                                additional_field3='First edition')
        doc22 = DocumentInstance.objects.create(document=doc2, status='a', location=location3, price=1700.0,
                                                additional_field1='Addison-Wesley Professional',
                                                additional_field2='2003',
                                                additional_field3='First edition')
        doc23 = DocumentInstance.objects.create(document=doc2, status='a', location=location3, price=1700.0,
                                                additional_field1='Addison-Wesley Professional',
                                                additional_field2='2003',
                                                additional_field3='First edition')

        doc3 = Document.objects.create(title='The Mythical Man-month',
                                       description='Few books on software project management have been as influential and timeless as The Mythical Man-Month. With a blend of software engineering facts and thought-provoking opinions, Fred Brooks offers insight for anyone managing complex projects. These essays draw from his experience as project manager for the IBM System/360 computer family and then for OS/360, its massive software system. Now, 20 years after the initial publication of his book, Brooks has revisited his original ideas and added new thoughts and advice, both for readers already familiar with his work and for readers discovering it for the first time.',
                                       type=type_book, is_reference=True)
        doc3.authors.add(author9)
        doc3.authors.add(author10)
        doc3.tags.add(tag1)
        doc3.tags.add(tag2)
        doc31 = DocumentInstance.objects.create(document=doc3, status='a', location=location2, price=100.0,
                                                additional_field1='Addison-Wesley Longman Publishing Co., Inc.',
                                                additional_field2='1995', additional_field3='Second edition')

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

    def test_case1(self):
        a = DocumentInstance.objects.filter(additional_field1='Spielberg')
        print(a)
        self.assertTrue(a)
        # tt = datetime.datetime.strptime('26 Sep 2012', '%d %b %Y')
        # doc11.DEBUG_give_out(doc1, patr1, patr_info1, datetime.datetime.strptime('31 Mar 2018', '%d %b %Y'))
        # doc21.DEBUG_give_out(doc1, s, patr_infos, datetime.datetime.strptime('31 Mar 2018', '%d %b %Y'))
        # doc22.DEBUG_give_out(doc1, v, patr_infov, datetime.datetime.strptime('31 Mar 2018', '%d %b %Y'))
