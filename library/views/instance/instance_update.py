from django.shortcuts import render, redirect, get_object_or_404
from library.forms import DocumentInstanceUpdate
from library.models import DocumentInstance, Reservation
from django.contrib.auth.decorators import permission_required


@permission_required("library.change_documentinstance")
def instance_update(request, id):
    instance = get_object_or_404(DocumentInstance, id=id)
    instance.document.quantity_synced = False
    instance.document.save()
    old_status = instance.status
    form = DocumentInstanceUpdate(request.POST or None, instance=instance)
    addfield = instance.document.type.fields
    addfield = addfield.split(';')
    if form.is_valid():
        form.save()
        if old_status == 'r':
            if form.instance.status != 'r':
                reservations = Reservation.objects.all()
                for log in reservations:
                    if log.document_copy.id == form.instance.id:
                        log.delete()
        return redirect('document-detail', id=instance.document.pk)
    return render(request, 'documentinstance_update.html', {'form': form, 'addfield': addfield})
