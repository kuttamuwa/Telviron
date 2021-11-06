from django.shortcuts import render
from django.template import loader
from rest_framework import status
from rest_framework.renderers import AdminRenderer
import pandas as pd
from rest_framework.request import override_method

from provider.models.models import Doviz


# todo: FutureImplementation

class TabelaRenderer(AdminRenderer):
    format = 'tabela'

    def get_context(self, data, accepted_media_type, renderer_context):
        """
        Render the HTML for the browsable API representation.
        """
        context = super().get_context(
            data, accepted_media_type, renderer_context
        )

        paginator = getattr(context['view'], 'paginator', None)
        if paginator is not None and data is not None:
            try:
                results = paginator.get_results(data)
            except (TypeError, KeyError):
                results = data
        else:
            results = data

        if results is None:
            header = {}
            style = 'detail'
        elif isinstance(results, list):
            header = results[0] if results else {}
            style = 'list'
        else:
            header = results
            style = 'detail'

        columns = [key for key in header if key != 'url']
        details = [key for key in header if key != 'url']

        if isinstance(results, list) and 'view' in renderer_context:
            for result in results:
                url = self.get_result_url(result, context['view'])
                if url is not None:
                    result.setdefault('url', url)

        context['style'] = style
        context['columns'] = columns
        context['details'] = details
        context['results'] = results
        context['error_form'] = getattr(self, 'error_form', None)
        context['error_title'] = getattr(self, 'error_title', None)
        return context
