from django.shortcuts import render, redirect


def index(request):
    """
    home page template
    """
    if request.user.is_authenticated:
        return redirect('document')
    else:
        return render(request, 'index.html')
