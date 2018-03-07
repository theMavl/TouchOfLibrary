import datetime
from django.contrib import auth
from django.shortcuts import render

from library.models import Document, DocumentInstance, PatronInfo, Reservation, GiveOut


def get_document_detail(request, id):
    """
    page with information about document
    """

    user = auth.get_user(request)
    document = Document.objects.get(id=id)
    additional = document.type.fields.split(sep=";")
    copy_list = DocumentInstance.objects.filter(document_id=id)
    if user.is_authenticated:
        patron = PatronInfo.objects.filter(user_id=user.id)
        if not patron:
            return render(request, 'library/document_detail.html',
                          context={"document": document, "additional": additional,
                                   "copy_list": copy_list, "not_a_patron": True})
        patron = patron.first()
        if not document.is_reference:
            if patron.patron_type.privileges:
                max_days = document.type.max_days_privileges
            else:
                if document.bestseller:
                    max_days = document.type.max_days_bestseller

                else:
                    max_days = document.type.max_days
            due_date = (datetime.date.today() + datetime.timedelta(max_days)).strftime("%d %b %Y")
        else:
            max_days = 0
            due_date = ""
        all_reserved = Reservation.objects.filter(user_id=user.id)
        all_checked_out = GiveOut.objects.filter(user_id=user.id)
        if patron.patron_type.max_documents > len(all_reserved) + len(all_checked_out):
            can_reserve = True
        else:
            can_reserve = False


        reserved = Reservation.objects.filter(user_id=user.id, document_id=document.id)
        given_out = GiveOut.objects.filter(user=user, document=document)
        return render(request, 'library/document_detail.html',
                      context={'given_out': given_out.first(),
                               'reserved': reserved,
                               "document": document,
                               "additional": additional,
                               "copy_list": copy_list,
                               "max_days": max_days,
                               "due_date": due_date,
                               "can_reserve": can_reserve})
    else:
        return render(request, 'library/document_detail.html',
                      context={"document": document, "additional": additional,
                               "copy_list": copy_list, "not_a_patron": True})
