from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from library.models import Document, DocumentInstance, Reservation, GiveOut, PatronInfo


@login_required
def reserve_document(request, copy_id):
    user = auth.get_user(request)
    patron = PatronInfo.objects.filter(user=user)
    copy = DocumentInstance.objects.get(id=str(copy_id))
    document = Document.objects.get(id=copy.document_id)

    if user.is_authenticated and user.is_active and patron and patron.first().patron_type is not None:
        reserved = Reservation.objects.filter(user_id=user.id, document_copy_id=copy.id)
        checked_out = GiveOut.objects.filter(user=user, document=document)
        if reserved:
            reserved.delete()
            copy.status = "a"
        elif not checked_out:
            copy.reserve(user)
        document.quantity_synced = False
        copy.save()
        document.save()
    return redirect('document-detail', id=document.id)
