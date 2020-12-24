from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams' 
        
    def __str__(self):
        return self.name
    
    def get_team_members_count(self):
        return len(Profile.objects.filter(team=self))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=255, null=True)
    profile_image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
