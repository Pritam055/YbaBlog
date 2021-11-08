from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.utils.text import slugify
from django.urls import reverse 
from django.contrib.auth.models import User 


# Create your models here.

# class Author(models.Model):
#     first_name = models.CharField(max_length = 50)
#     last_name = models.CharField(max_length = 50)
#     email_address = models.EmailF

class Post(models.Model):
    title = models.CharField(max_length = 180)
    date_time = models.DateTimeField(auto_now =True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    slug = models.SlugField(max_length=255,unique=True,  blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    vote_count = models.PositiveIntegerField(default = 0 )
    voter = models.ManyToManyField(User)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.slug})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 400)
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.title}"

""" class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    vote_count = models.PositiveIntegerField(default=0)
    voters_username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.post.title} - {self.vote_count}" """
 