from django.shortcuts import render, redirect

from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy, reverse
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
    # success_url = reverse_lazy('provider')
    success_message = '{doviz} başarıyla güncellendi'

    # def get_success_url(self):
    #     messages.add_message(self.request, messages.SUCCESS, 'Başarıyla kaydedildi')
    #     return reverse('provider:')

    def form_valid(self, form):
        response = super(DovizView, self).form_valid(form)
        success_messages = self.get_success_message(form.cleaned_data)

        if success_messages:
            messages.success(self.request, success_messages)

        return response

    def get_success_message(self, cleaned_data):
        return self.success_message.format(doviz=cleaned_data.get('kur'))

    def get_success_url(self):
        return self.request.path
