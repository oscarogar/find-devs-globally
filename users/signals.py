from django.db.models.signals import post_save, post_delete
#the receiver is a decorator that connects the signals
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


 #@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
        if created:
            user = instance
            profile = Profile.objects.create(
                user = user,
                username = user.username,

                name = user.first_name,
                email = user.email,
            )
            try:
                subject = "Welcome to Oscar's Website Playground"
                message = "Made with Django as a personal Project for potential employers"

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [profile.email],
                    fail_silently=False,
                )
            except:
                pass



def updateProfile(sender, instance, created, **kwargs):
        profile = instance
        user = profile.user
        if created == False:
                user.username = profile.username
                user.first_name = profile.name
                user.email = profile.email
                user.save()

def deleteUser(sender, instance, **kwargs):
        try:
            user = instance.user
            user.delete()
        except:
            pass
post_save.connect(updateProfile, sender=Profile)
post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)