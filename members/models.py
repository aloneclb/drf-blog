from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# signals
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # user.profile
    bio = models.CharField(max_length=300, null=True, blank=True)
    sehir = models.CharField(max_length=300, null=True, blank=True)
    foto = models.ImageField(upload_to = 'profils/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.user.username + ' Profili'

    def save(self, *args, **kwargs):
        ## İmage Resize
        super(Profile, self).save(*args, **kwargs)
        if self.foto:
            img = Image.open(self.foto.path)
            if img.height > 600 or img.width > 600:
                output_size = (600,600)
                img.thumbnail(output_size)
                img.save(self.foto.path)


class ProfileMessage(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=240)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_profile) + ' Durumu'




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save, sender=Profile)
def create_profile_message(sender, instance, created, **kwargs):
    if created:
        ProfileMessage.objects.create(user_profile = instance, body=f'{instance.user.username} welcome to the program...')
        