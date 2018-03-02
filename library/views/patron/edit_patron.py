from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from library.forms import EditPatron, AddPatron
from library.models import PatronInfo


@permission_required('auth.change_user')
def edit_patron(request, pk):
    if request.method == 'POST':
        form = EditPatron(request.POST)

        if form.is_valid():
            edited_user = User.objects.get(id=pk)
            edited_patron_info = PatronInfo.objects.get(user_id=pk)

            edited_user.email = form.cleaned_data['email']
            edited_user.first_name = form.cleaned_data['name']
            edited_user.last_name = form.cleaned_data['surname']
            edited_user.save()

            edited_patron_info.phone_number = form.cleaned_data['phone_number']
            edited_patron_info.address = form.cleaned_data['address']
            edited_patron_info.telegram = form.cleaned_data['telegram']
            edited_patron_info.patron_type = form.cleaned_data['type']
            edited_patron_info.save()

            return HttpResponseRedirect('/library/patrons/' + str(pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        patron = PatronInfo.objects.get(user_id=pk)
        form = EditPatron(initial={'username': patron.user.username,
                                   'name': patron.user.first_name, 'surname': patron.user.last_name,
                                   'email': patron.user.email, 'phone_number': patron.phone_number,
                                   'telegram': patron.telegram, 'address': patron.address,
                                   'type': patron.patron_type})

    return render(request, 'library/patron_edit.html', {'form': form})
