from django.db import models

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=255)
    sf_id = models.CharField(max_length=16, unique=True)
    content_html = models.TextField()
    content = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("Tag")
    create_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Answer(models.Model):
    content_html = models.TextField()
    content = models.TextField(blank=True, null=True)
