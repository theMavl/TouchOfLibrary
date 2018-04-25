from django.shortcuts import render, redirect
from library.forms import TagCreate
from django.contrib.auth.decorators import permission_required

from library.models import Tag


@permission_required('library.add_tag')
def tag_create(request):
    instance = Tag.objects.create()
    form = TagCreate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        instance.save()

        from library.logger import create_log
        create_log(request, "Created", instance)

        return redirect('tags')
    instance.delete()
    return render(request, 'tag_create.html', {'form': form})
