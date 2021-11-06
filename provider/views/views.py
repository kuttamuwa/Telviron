from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView

from provider.forms.doviz import DovizForm


def main_page(request):
    return render(request, 'provider/provider.html')


def admin_page(request):
    return render(request, 'provider/set_doviz.html')


def kur_page(request):
    return render(request, 'provider/get_doviz.html')


class DovizView(FormView):
    template_name = 'provider/set_doviz.html'
    form_class = DovizForm

    def form_valid(self, form):
        return super(DovizView, self).form_valid(form)

