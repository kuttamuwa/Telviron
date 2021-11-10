from django.db import models

# import pandas as pd


class MakasFilter(models.Manager):
    """
    Based on Pandas Dataframe
    """

    def filter(self, *args, **kwargs):
        qset = super(MakasFilter, self).filter(*args, **kwargs)
        # df = pd.Dataframe(qset.values())

        return qset

    def get_queryset(self):
        qset = super(MakasFilter, self).get_queryset()
        # df = pd.Dataframe(qset.values())

        return qset

    def filter_ozbey(self):
        qset = self.filter(source='Ozbey')
        # df = pd.DataFrame(qset.values())

        # makas_qset = Makas.objects.order_by('kur')
        # makas_df = pd.DataFrame(makas_qset.values())

        return qset
