from django.shortcuts import redirect, get_object_or_404, render

from library.models import DocType, Document


def type_deleteconfirm(request, id):
    instance = get_object_or_404(DocType, id=id)
    docs = Document.objects.all()
    count = 0
    for doc in docs:
        if str(doc.type.name) == str(instance.name):
            count += 1
    return render(request, 'type_deleteconfirm.html', {'instance': instance, 'id': id, 'count' : count})


def type_delete(request, id):
    instance = get_object_or_404(DocType, id=id)

    instance = get_object_or_404(DocType, id=id).delete()
    return redirect('types')
