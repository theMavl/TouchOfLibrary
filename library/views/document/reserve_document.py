from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from library.models import Document, DocumentInstance, Reservation, GiveOut, User


@login_required
def reserve_document(request, copy_id):
    user = auth.get_user(request)
    copy = DocumentInstance.objects.get(id=str(copy_id))
    document = Document.objects.get(id=copy.document_id)

    if user.is_authenticated and user.is_active and not user.is_limited and user.is_patron:
        reserved = Reservation.objects.filter(user_id=user.id, document_copy_id=copy.id)
        checked_out = GiveOut.objects.filter(user=user, document=document)
        if reserved:
            reserved.delete()
            copy.status = "a"
            copy.reserve_from_queue(request)
        elif not checked_out:
            copy.reserve(request, user, False)
        document.quantity_synced = False
        copy.save()
        document.save()

        from library.logger import create_log
        create_log(request, "Reserved", copy)

    return redirect('document-detail', id=document.id)
