from django.shortcuts import render, redirect, get_object_or_404

from library.forms import TypeUpdate
from library.models import DocType


def type_update(request, id):
    instance = get_object_or_404(DocType, id=id)
    form = TypeUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('types-detail', pk=form.instance.id)
    return render(request, 'type_update.html', {'form': form})
