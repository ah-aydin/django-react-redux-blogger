from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    return f'images/{filename}'

class Blog(models.Model):
    title           = models.CharField(max_length=255, unique=True)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body            = models.TextField()
    title_image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    # Information about the blog
    date_created    = models.DateField(auto_now_add=True)
    date_modified   = models.DateField(auto_now=True) 
  
    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.PROTECT)
    blog            = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    body            = models.TextField()
    
    # Information about the comment
    date_created    = models.DateField(auto_now_add=True)
    date_modified   = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.blog.title}'