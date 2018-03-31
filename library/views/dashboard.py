from django.shortcuts import render
from library.models import PatronInfo, Reservation, GiveOut, GiveOutLogEntry, DocumentRequest
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import cloudinary


@login_required
def dashboard(request):
    image = cloudinary.CloudinaryImage("sample2.jpg")
    user = auth.get_user(request)
    try:
        patron = PatronInfo.objects.get(user_id=user.id)
    except:
        patron = None
    reservation_list = Reservation.objects.filter(user_id=user.id)
    giveout_list = GiveOut.objects.filter(user_id=user.id)
    giveout_log_list = GiveOutLogEntry.objects.filter(user_id=user.id)
    request_list = DocumentRequest.objects.filter(user_id=user.id)

    return render(
        request,
        'dashboard.html',
        context={'patron_user': user,
                 'patron_info': patron,
                 'reservation_table': reservation_list,
                 'giveout_table': giveout_list,
                 'giveout_log_table': giveout_log_list,
                 'request_table': request_list,
                 'image': image},
    )