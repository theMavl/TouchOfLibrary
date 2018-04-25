from django.shortcuts import render, redirect
from library.forms import TypeCreate
from library.models import DocType
from django.contrib.auth.decorators import permission_required


@permission_required('library.add_doctype')
def type_create(request):
    instance = DocType.objects.create()
    form = TypeCreate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        from library.logger import create_log
        create_log(request, "Created", instance)

        return redirect('types')
    instance.delete()
    return render(request, 'type_create.html', {'form': form})
