from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile
''' signals.py in a Django application is typically used to define custom signals and signal handlers. 
Signals in Django are a mechanism for allowing certain senders to notify a set of receivers 
when certain actions occur. '''


# creates a UserProfile for a newly created User instance or updates an existing one upon saving
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the user profile if not exist
            UserProfile.objects.create(user=instance)

# a placeholder for potential future actions before saving a User instance
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
