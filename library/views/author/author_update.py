from django.shortcuts import render, redirect, get_object_or_404

from library.forms import AuthorUpdate
from library.models import Author


def author_update(request, id):
    instance = get_object_or_404(Author, id=id)
    form = AuthorUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('author-detail', pk=form.instance.id)
    return render(request, 'author_update.html', {'form': form})
