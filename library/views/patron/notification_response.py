from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from library.models import Reservation


@login_required
def notification_response(request, id):
    reservation = Reservation.objects.filter(id=id)
    if reservation:
        user = auth.get_user(request)
        reservation = reservation.first()
        if user.id == reservation.user_id:
            reservation.confirmed = True
            reservation.save()
            return HttpResponse(
                "We've received your confirmation, thank you! Don't forget to take your document in time.")
        else:
            return HttpResponse('Access denied')
    else:
        return HttpResponse('Bad link')
