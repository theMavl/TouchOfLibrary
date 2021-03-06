import datetime
from django.contrib import auth
from django.shortcuts import render

from library.models import Document, DocumentInstance, Reservation, GiveOut, DocumentRequest


def get_document_detail(request, id):
    """
    page with information about document
    """

    user = auth.get_user(request)
    document = Document.objects.get(id=id)
    additional = document.type.fields.split(sep=";")
    copy_list = DocumentInstance.objects.filter(document_id=id)
    all_given_out = copy_list.filter(status='g')
    print(all_given_out.count())
    image = document.image
    if user.is_authenticated:
        if not user.is_patron:
            return render(request, 'library/document_detail.html',
                          context={"document": document, "image": image, "additional": additional,
                                   "copy_list": copy_list,
                                   'all_given_out': all_given_out,
                                   "not_a_patron": True})
        if not document.is_reference:
            max_days = document.days_available(user)
            due_date = (datetime.date.today() + datetime.timedelta(max_days)).strftime("%d %b %Y")
        else:
            max_days = 0
            due_date = ""
        all_reserved = Reservation.objects.filter(user_id=user.id)
        all_checked_out = GiveOut.objects.filter(user_id=user.id)
        if not user.is_patron or user.patron_type is None or user.is_limited:
            can_reserve = False
            reservation_limit = False
        else:
            can_reserve = True
            if user.patron_type.max_documents > len(all_reserved) + len(all_checked_out):
                reservation_limit = False
            else:
                reservation_limit = True

        reserved = Reservation.objects.filter(user_id=user.id, document_id=document.id)
        given_out = GiveOut.objects.filter(user=user, document=document)
        requested = DocumentRequest.objects.filter(user=user, document=document)
        return render(request, 'library/document_detail.html',
                      context={'all_given_out': all_given_out,
                               'given_out': given_out.first(),
                               'reserved': reserved,
                               'requested': requested,
                               "document": document,
                               "image": image,
                               "additional": additional,
                               "copy_list": copy_list,
                               "max_days": max_days,
                               "due_date": due_date,
                               "can_reserve": can_reserve,
                               "reservation_limit": reservation_limit})
    else:
        return render(request, 'library/document_detail.html',
                      context={"document": document,
                               "image": image, "additional": additional,
                               "copy_list": copy_list,
                               'all_given_out': all_given_out,
                               "can_reserve": False})
