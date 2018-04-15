from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from library.forms import EditPatron
from library.models import User


@permission_required('auth.change_user')
def edit_patron(request, pk):
    if request.method == 'POST':
        form = EditPatron(request.POST)

        if form.is_valid():
            edited_patron = User.objects.get(id=pk)

            edited_patron.email = form.cleaned_data['email']
            edited_patron.first_name = form.cleaned_data['name']
            edited_patron.last_name = form.cleaned_data['surname']
            edited_patron.save()

            edited_patron.phone_number = form.cleaned_data['phone_number']
            edited_patron.address = form.cleaned_data['address']
            edited_patron.telegram = form.cleaned_data['telegram']
            edited_patron.patron_type = form.cleaned_data['type']
            edited_patron.save()

            return HttpResponseRedirect('/library/patrons/' + str(pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        patron = User.objects.get(id=pk)
        form = EditPatron(initial={'username': patron.username,
                                   'name': patron.first_name, 'surname': patron.last_name,
                                   'email': patron.email, 'phone_number': patron.phone_number,
                                   'telegram': patron.telegram, 'address': patron.address,
                                   'type': patron.patron_type})

    return render(request, 'library/patron_edit.html', {'form': form})
