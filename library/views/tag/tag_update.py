from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from library.forms import TagUpdate
from library.models import Tag


@permission_required('library.change_tag')
def tag_update(request, id):
    instance = get_object_or_404(Tag, id=id)
    form = TagUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        from library.logger import create_log
        create_log(request, "Updated", instance)

        return redirect('tags')
    return render(request, 'tag_update.html', {'form': form})
