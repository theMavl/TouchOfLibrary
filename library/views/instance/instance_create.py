from django.shortcuts import render, redirect
from library.forms import DocumentInstanceCreate
from library.models import Document, DocumentInstance
from django.contrib.auth.decorators import permission_required


@permission_required("library.add_documentinstance")
def instance_create(request, pk):
    instance = DocumentInstance.objects.create()
    docs = Document.objects.all()
    current_doc = None
    for doc in docs:
        if str(doc.pk) == pk:
            current_doc = doc
    addfield = current_doc.type.fields.split(';')
    form = DocumentInstanceCreate(request.POST or None, instance=instance)
    if form.is_valid():
        form.instance.document = current_doc
        form.save()
        doc_id = form.instance.document.id
        current_doc.quantity_synced = False
        current_doc.save()
        return redirect('document-detail', id=doc_id)
    instance.delete()
    return render(request, 'documentinstance_create.html',
                  {'form': form, 'addfield': addfield, 'current_doc': current_doc})
