from django.db.models.query_utils import refs_expression
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.contrib.auth.models import User 
import os 
from django.dispatch import receiver 

from .models import Profile

# @receiver(post_save, sender=User)
def profile_create_handler(sender, instance, created,**kwargs):
    if created: 
        # p = Profile(user=instance)
        # p.save()
        Profile.objects.create(user=instance)
        
post_save.connect(profile_create_handler, sender=User)
 
# @receiver(pre_delete, sender=Profile)
def delete_image_handler(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path 
        os.remove(image_path)
    # print("Pre delete called")
pre_delete.connect(delete_image_handler, sender=Profile)

# check if image is updated and delete the previous image if updated
# @receiver(pre_save, sender=Profile)
""" def check_profile_image_update(sender, instance, raw,  **kwargs):
    print(instance.user)
    print(type(instance)) 
    print(instance.image)
    print(instance.image == "") 
    print(instance.image is None) 
    print(instance is None) 
    print(instance.pk)
    p = Profile.objects.get(user=instance.user)
    print(p)
    # if instance.image.path == "": # check if image already exists or not
    #     pass 
    # else: 
    #     previous = Profile.objects.get(user=instance.user)
    #     # print(previous.image, previous.image=="")
    #     # print(instance.image, instance.image=="")
    #     # print(instance.image == previous.image)
    #     if previous.image != instance.image:
    #         image_path = previous.image.path
    #         os.remove(image_path)
pre_save.connect(check_profile_image_update, sender=Profile) """

# delete User object also white deleting profile object from the admin panel
def delete_user_object_simultaneously(sender, instance, **kwargs): 
    if instance.user:
        instance.user.delete()
post_delete.connect(delete_user_object_simultaneously, sender=Profile)

 