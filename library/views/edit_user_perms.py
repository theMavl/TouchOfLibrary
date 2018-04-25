from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render

from library.forms import EditUserPerms
from library.models import User


@permission_required('library.change_user')
def edit_user_perms(request, pk):
    all_groups = Group.objects.all()
    edited_user = User.objects.get(id=pk)
    perms = []

    for group in all_groups:
        perms.append( [group.name, [x.name for x in group.permissions.all()]] )

    if request.method == 'POST':
        form = EditUserPerms(request.POST)

        if form.is_valid():

            for group in edited_user.groups.all():
                group.user_set.remove(edited_user)

            for group in form.cleaned_data['groups']:
                edited_user.groups.add(group)

            edited_user.save()

            from library.logger import create_log
            if edited_user.is_patron:
                create_log(request, "Redefine Group", edited_user)

            return HttpResponseRedirect('/library/patrons/' + str(pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUserPerms(initial={'groups': edited_user.groups.all()})
        print(perms)

    return render(request, 'library/edit_user_perms.html', {'form': form, 'edited_user': edited_user, 'perms': perms})
