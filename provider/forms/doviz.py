from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from django import forms

from provider.models.models import Doviz


class DovizForm(forms.Form):
    kur = forms.CharField(required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'Kur değeri: USDTRY, EURUSD, KGRTRY vs.'}),
                          help_text='Kur veya sarrafiye kısaltması giriniz. Örneğin : USDTRY',
                          initial='USDTRY')

    alis = forms.FloatField(required=True, min_value=0,
                            widget=forms.NumberInput(attrs={'placeholder': 'Alış fiyatını nokta kullanarak giriniz',
                                                            'step': '0.1'}),
                            initial='1.2'

                            # help_text='Alış fiyatını giriniz'
                            )
    satis = forms.FloatField(required=True, min_value=0,
                             widget=forms.NumberInput(attrs={'placeholder': 'Satış fiyatını nokta kullanarak giriniz',
                                                             'step': '0.1'},
                                                      ),
                             initial='1.5'
                             # help_text='Satış fiyatını giriniz'
                             )

    source = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '(varsa) Veri kaynağınızı giriniz'}),
                             help_text='Tercihen'
                             )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        # self.helper.form_action
        self.helper.form_tag = False

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

        self.helper.layout = Layout(
            Row(
                Column('kur', css_class='form-group col-md-6 mb-0'),
                Column('alis', css_class='form-group col-md-6 mb-0'),
                Column('satis', css_class='form-group col-md-6 mb-0'),
                Column('kaynak', css_class='form-group col-md-6 mb-0'),
            ),

        )



