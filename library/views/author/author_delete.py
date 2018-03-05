from django.shortcuts import redirect, get_object_or_404, render

from library.models import Author


def author_deleteconfirm(request, id):
    instance = get_object_or_404(Author, id=id)
    return render(request, 'author_deleteconfirm.html', {'instance': instance, 'id': id})


def author_delete(request, id):
    instance = get_object_or_404(Author, id=id)
    instance = get_object_or_404(Author, id=id).delete()
    return redirect('authors')
