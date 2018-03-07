from django.shortcuts import render, redirect
from library.forms import TagCreate
from django.contrib.auth.decorators import permission_required


@permission_required('library.add_tag')
def tag_create(request):
    form = TagCreate(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tags')
    return render(request, 'tag_create.html', {'form': form})
