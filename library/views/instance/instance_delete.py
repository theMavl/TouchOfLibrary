from django.shortcuts import redirect, get_object_or_404

from library.models import DocumentInstance


def instance_delete(request, id):
    instance = get_object_or_404(DocumentInstance, id=id)
    instance.document.quantity_synced = False
    instance.document.save()
    copy = instance.document.id
    instance = get_object_or_404(DocumentInstance, id=id).delete()
    return redirect('document-detail', id=copy)
