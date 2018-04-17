from django.contrib.auth import login
from library.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from library.forms import SignupForm
from library.tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            message = render_to_string('mails/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': str(urlsafe_base64_encode(force_bytes(user.pk)))[2:-1],
                'token': account_activation_token.make_token(user),
            })
            user.email_user('Touch of Library: Account activation', message)

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_patron = True
        user.is_limited = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse(
            'Thank you for your email confirmation. Registration is complete. '
            'However, your account have limited rights. '
            'In order to confirm your patron card, please visit Touch of Library.')
    else:
        return HttpResponse('Activation link is invalid!')
