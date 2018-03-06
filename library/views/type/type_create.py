from django.shortcuts import render, redirect
from library.forms import TypeCreate
from library.models import DocType


def type_create(request):
    instance = DocType.objects.create()
    form = TypeCreate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('types')
    instance.delete()
    return render(request, 'type_create.html', {'form': form})
