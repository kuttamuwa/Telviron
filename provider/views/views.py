from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(request, 'provider/provider.html')


def admin_page(request):
    return render(request, 'provider/set_doviz.html')


def kur_page(request):
    return render(request, 'provider/get_doviz.html')
