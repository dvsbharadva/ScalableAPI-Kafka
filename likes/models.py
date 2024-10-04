from django.db import models

# Create your models here.
class Likes(models.Model):
    post = models.CharField(max_length=64)
    like = models.BigIntegerField(default=0)
    
    def __str__(self) -> str:
        return f" {self.post} - likes : {self.like}"
    