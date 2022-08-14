from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class userHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sh = models.JSONField(default={"data": []})
    lh = models.JSONField(default={"data": []})

    def __str__(self):
        return self.user.username
