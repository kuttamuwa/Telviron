from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from provider.models.models import Doviz, SarrafiyeMilyem, DovizH, SarrafiyeMilyemH


@receiver(pre_save, sender=Doviz)
def doviz_log_changes(sender, **kwargs):
    instance = kwargs['instance']
    print(f"Döviz tablosunda değişiklik yapılıyor ! : {instance}")

    try:
        old_doviz = Doviz.objects.get(id=instance.id)

        DovizH.objects.create(
            instance=old_doviz,
            old_alis=old_doviz.alis,
            old_satis=old_doviz.satis
        )
    except Doviz.DoesNotExist:
        print("ilk defa kayit ekleniyor")


@receiver(post_save, sender=SarrafiyeMilyem)
def sarrafiye_log_changes(sender, **kwargs):
    instance = kwargs['instance']
    print("Sarrafiye tablosunda değişiklik yapılıyor !")

    try:
        old_sarraf = SarrafiyeMilyem.objects.get(id=instance.id)
        SarrafiyeMilyemH.objects.create(
            instance=instance,
            old_alis=old_sarraf.alis,
            old_satis=old_sarraf.satis
        )

    except SarrafiyeMilyem.DoesNotExist:
        print("ilk defa kayıt ekleniyor")