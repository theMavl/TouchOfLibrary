from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from library.forms import AddPatron
from library.models import User


@permission_required('library.add_patron')
def add_patron(request):
    if request.method == 'POST':
        form = AddPatron(request.POST)

        if form.is_valid():
            password = User.objects.make_random_password()
            created_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    email=form.cleaned_data['email'],
                                                    password=password,
                                                    first_name=form.cleaned_data['name'],
                                                    last_name=form.cleaned_data['surname'],
                                                    is_patron=True,
                                                    phone_number=form.cleaned_data['phone_number'],
                                                    address=form.cleaned_data['address'],
                                                    telegram=form.cleaned_data['telegram'],
                                                    patron_type=form.cleaned_data['type'])

            return render(request, 'library/registration_info.html',
                          {'username': created_user.username, 'password': password, 'email': created_user.email,
                           'patron_id': created_user.id,
                           'full_name': created_user.first_name + " " + created_user.last_name,
                           'phone': created_user.phone_number, 'address': created_user.address,
                           'telegram': created_user.telegram,
                           'patron_type': created_user.patron_type})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddPatron(initial={'name': "", 'surname': "",
                                  'email': "",
                                  'telegram': "@", 'password': ''})

    return render(request, 'library/patron_add.html', {'form': form})
