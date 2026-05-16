from django.apps import AppConfig


class HelplyConfig(AppConfig):
    name = "helply"

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .models import Profile

        def create_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.get_or_create(user=instance, defaults={'role': 'helper'})

        post_save.connect(create_profile, sender=User)