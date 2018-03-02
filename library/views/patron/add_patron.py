from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from library.forms import AddPatron
from library.models import PatronInfo


@permission_required('auth.add_user')
def add_patron(request):
    if request.method == 'POST':
        form = AddPatron(request.POST)

        if form.is_valid():
            created_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    email=form.cleaned_data['email'],
                                                    password=form.cleaned_data['password'],
                                                    first_name=form.cleaned_data['name'],
                                                    last_name=form.cleaned_data['surname'])
            PatronInfo.objects.create(user=created_user,
                                      phone_number=form.cleaned_data['phone_number'],
                                      address=form.cleaned_data['address'],
                                      telegram=form.cleaned_data['telegram'],
                                      patron_type=form.cleaned_data['type'])

            return HttpResponseRedirect('/library/patrons/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddPatron(initial={'name': "", 'surname': "",
                                  'email': "", 'phone_number': '8',
                                  'telegram': "@", 'password': ''})

    return render(request, 'library/patron_add.html', {'form': form})
