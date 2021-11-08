from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
import os 

from .models import Post

""" 
=> Using singal in different file we need to configuration which can be done in two ways.
=> 1) either do configuration in apps.py and __init__.py
=> 2) configure in settings.py file in Installed_apps section as: 'blog.apps.BlogConfig'
 """

# --handler to automatic remove image when model is deleted
# @receiver(pre_delete, sender=Post )
def delete_image_handler(sender, instance, *args, **kwargs):
    if instance.image:
        image_path = instance.image.path 
        os.remove(image_path)
    # print("Pre delete called")

pre_delete.connect(delete_image_handler, sender=Post)

""" def create_vote_object(sender, instance, created, *args, **kwargs):
    vote = Vote(post=instance)
    vote.save()
post_save.connect(create_vote_object, sender=Post) """