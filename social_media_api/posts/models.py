from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author =models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_named="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeFiels(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class CustomUser(AbstractUser):
    #users that this user follows
    following = models.ManyToManyField(
        'self',
        symmetrical=False, #one-way relationship
        related_name='followers',
        blank=True
    )    
    def __str__(self):
        return self.username

    

