from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from library.models import Document, DocumentRequest, Reservation, GiveOut


@login_required
def request_document(request, document_id):
    user = auth.get_user(request)
    document = Document.objects.get(id=document_id)

    if document.quantity() > 0:
        redirect('document-detail', id=document_id)

    if user.is_authenticated and user.is_active and user.is_patron:
        requested = DocumentRequest.objects.filter(user_id=user.id, document_id=document_id)
        reserved = Reservation.objects.filter(user_id=user.id, document_id=document_id)
        checked_out = GiveOut.objects.filter(user=user, document=document)
        if requested:
            instance = requested.first()
            from library.logger import create_log
            create_log(request, "Canceled", instance)
            requested.delete()

        elif not checked_out and not reserved and not document.is_reference:
            DocumentRequest.objects.create(user=user, document=document).save()

            from library.logger import create_log
            create_log(request, "Requested", document)

    return redirect('document-detail', id=document_id)
