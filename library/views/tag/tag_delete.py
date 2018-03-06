from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import permission_required
from library.models import Tag, Document


@permission_required('library.delete_tag')
def tag_deleteconfirm(request, id):
    instance = get_object_or_404(Tag, id=id)
    all_docs = Document.objects.all()
    wrong_docs = []
    for docs in all_docs:
        if docs.tags.filter(id=id).count() != 0:
            wrong_docs.append(docs)

    return render(request, 'tag_deleteconfirm.html', {'instance': instance, 'id': id, 'wrong_docs': wrong_docs})


@permission_required('library.delete_tag')
def tag_delete(request, id):
    instance = get_object_or_404(Tag, id=id)
    instance.delete()
    return redirect('tags')
