from django.shortcuts import render, redirect
from library.forms import AuthorCreate
from library.logger.logger import create_log
from django.contrib.auth.decorators import permission_required

from library.models import Author


@permission_required('library.add_author')
def author_create(request):
    instance = Author.objects.create()
    form = AuthorCreate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        create_log(request, "Created", instance)
        return redirect('authors')
    instance.delete()
    return render(request, 'author_create.html', {'form': form})
