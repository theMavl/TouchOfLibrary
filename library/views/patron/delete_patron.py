from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from library.forms import DeletePatron
from library.models import PatronInfo


@permission_required('auth.delete_user')
def delete_patron(request, pk):
    if request.method == 'POST':
        form = DeletePatron(request.POST)

        if form.is_valid():
            current_user = User.objects.get(id=pk)
            current_patron = PatronInfo.objects.get(user_id=pk)

            current_user.delete()
            current_patron.delete()

            return HttpResponseRedirect('/library/patrons/')
    else:
        form = DeletePatron(initial={'comment': ''})
        return render(request, 'library/patron_delete.html', {'form': form})
    return redirect('document-detail', id=copy)
