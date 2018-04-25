from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import permission_required
from library.models import DocumentInstance


@permission_required("library.delete_documentinstance")
def instance_deleteconfirm(request, id):
    instance = get_object_or_404(DocumentInstance, id=id)
    return render(request, 'documentinstance_deleteconfirm.html', {'instance': instance, 'id': id})

@permission_required("library.delete_documentinstance")
def instance_delete(request, id):
    instance = get_object_or_404(DocumentInstance, id=id)
    instance.document.quantity_synced = False
    instance.document.save()
    copy = instance.document.id

    from library.logger import create_log
    create_log(request, "Removed", instance)

    instance = get_object_or_404(DocumentInstance, id=id).delete()
    return redirect('document-detail', id=copy)
