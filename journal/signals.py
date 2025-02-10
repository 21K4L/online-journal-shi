from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for user: {instance.username}")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print(f"Profile saved for user: {instance.username}")
    instance.profile.save()