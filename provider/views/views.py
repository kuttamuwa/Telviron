import datetime

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from rest_framework.renderers import TemplateHTMLRenderer, AdminRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from provider.forms.doviz import DovizForm
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets

from rest_pandas import PandasView
from rest_pandas.serializers import PandasSerializer

from provider.models.models import Doviz
from provider.models.serializers import DovizSerializer, HistorySerializer
from provider.views.renderers import TabelaRenderer


def main_page(request):
    return render(request, 'provider/provider.html')


def admin_page(request):
    return render(request, 'provider/set_doviz.html')


def kur_page(request):
    return render(request, 'provider/get_doviz.html')


class TabelaView(APIView):
    queryset = Doviz.objects.all()

    authentication_classes = [

    ]
    permission_classes = [

    ]

    renderer_classes = [
        AdminRenderer,
        TabelaRenderer

    ]

    def get_historical(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        # django ORM
        historical_doviz = Doviz.objects.values('kur', 'update_date', 'alis', 'satis')

        # pandas
        df = pd.DataFrame(historical_doviz)
        latest_df = df.sort_values('update_date').groupby('kur').head(2)  # last 2
        latest_df.reset_index(inplace=True)
        latest_df.rename(columns={'kur': 'Kur', 'update_date': 'Son tarih',
                                  'alis': 'Alış', 'satis': 'Satış'}, inplace=True)
        latest_df.drop(columns=['index'], inplace=True)

        # pandas : styling
        df_html = latest_df.style.format({'Alış': "{:.3f}",
                                          'Satış': "{:.3f}",
                                          'Son tarih': "{:%Y-%m-%d}"}).set_table_styles([
            {'selector': 'tr:hover'},
            {"selector": "", "props": [("border", "1px solid grey")]},
            {"selector": "tbody td", "props": [("border", "1px solid grey")]},
            {"selector": "th", "props": [("border", "1px solid grey")]}
        ])
        df_html = df_html.render()

        # rendering
        return render(request, 'provider/get_doviz.html', {'df': df_html})

    def get_pure(self, request, format=None):
        qset = Doviz.objects.all()
        serializer = DovizSerializer(qset, many=True)

        return Response(
            serializer.data, template_name='provider/get_doviz.html'
        )

    def get(self, request, format=None):
        history = bool(request.query_params.get('history', False))

        if history:
            return self.get_historical(request, format)

        else:
            return self.get_pure(request, format)


class DovizFormView(FormView):
    template_name = 'provider/set_doviz.html'
    form_class = DovizForm
    success_message = '{doviz} başarıyla güncellendi'

    def form_valid(self, form):
        response = super(DovizFormView, self).form_valid(form)
        success_messages = self.get_success_message(form.cleaned_data)

        if success_messages:
            messages.success(self.request, success_messages)

        return response

    def get_success_message(self, cleaned_data):
        return self.success_message.format(doviz=cleaned_data.get('kur'))

    def get_success_url(self):
        return self.request.path
