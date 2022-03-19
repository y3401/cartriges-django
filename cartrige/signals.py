from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Records,Nmax

@receiver(post_save, sender=Records)
def update_nmax(sender, instance, created, **kwargs):
    if created:
        nm = Nmax.objects.get(zapis=0)
        nm.nmax += 1
        nm.save()