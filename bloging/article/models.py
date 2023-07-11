from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.shortcuts import reverse
# Create your models here.

User = get_user_model()

class Article(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def get_api_url(self):
        try:
            return reverse("articles_api:post_detail", kwargs={"slug": self.slug})
        except:
            None

    @property
    def comments(self):
        instance = self
        qs = Comments.objects.filter(parent=instance)
        return qs
    
class Comments(models.Model):
    parent = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']



    