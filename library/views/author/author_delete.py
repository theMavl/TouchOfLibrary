from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from library.models import Author

@permission_required('library.delete_author')
def author_deleteconfirm(request, id):
    instance = get_object_or_404(Author, id=id)
    return render(request, 'author_deleteconfirm.html', {'instance': instance, 'id': id})

@permission_required('library.delete_author')
def author_delete(request, id):
    instance = get_object_or_404(Author, id=id)

    from library.logger import create_log
    create_log(request, "Deleted", instance)

    instance = get_object_or_404(Author, id=id).delete()
    return redirect('authors')
