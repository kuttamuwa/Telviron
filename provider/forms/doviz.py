from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms


class DovizForm(forms.Form):
    kur = forms.CharField(required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'Kur değeri: USDTRY, EURUSD, KGRTRY vs.'}),
                          help_text='Kur veya sarrafiye kısaltması giriniz. Örneğin : USDTRY')
    alis = forms.FloatField(required=True, min_value=0,
                            widget=forms.NumberInput(attrs={'step': '0.1'}),
                            help_text='Alış fiyatını giriniz')
    satis = forms.FloatField(required=True, min_value=0,
                             widget=forms.NumberInput(attrs={'step': '0.1'}),
                             help_text='Satış fiyatını giriniz')

    source = forms.CharField(required=False, widget=forms.TextInput(), help_text='(varsa) veri kaynağını giriniz')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(

        )
