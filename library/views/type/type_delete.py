from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from library.models import DocType, Document, DocumentInstance


@permission_required('library.delete_doctype')
def type_deleteconfirm(request, id):
    instance = get_object_or_404(DocType, id=id)
    docs = Document.objects.all()
    count = 0
    wrong_docs = []
    given_out = []
    for doc in docs:
        if str(doc.type.name) == str(instance.name):
            wrong_docs.append(doc)
            count += 1
    for doc in wrong_docs:
        copyes = DocumentInstance.objects.filter(document_id=doc.id)
        for copy in copyes:
            if copy.status == 'g':
                given_out.append(doc)
                wrong_docs.remove(doc)
                break
    return render(request, 'type_deleteconfirm.html', {'instance': instance,
                                                       'id': id,
                                                       'count': count,
                                                       'wrong_docs': wrong_docs,
                                                       'given_out': given_out})


@permission_required('library.delete_doctype')
def type_delete(request, id):
    instance = get_object_or_404(DocType, id=id)

    from library.logger import create_log
    create_log(request, "Removed", instance)

    instance = get_object_or_404(DocType, id=id).delete()
    return redirect('types')
