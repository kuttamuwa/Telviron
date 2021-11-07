from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(
        request,
        'base.html'
    )


def login_page(request):
    return render(request, 'login.html')