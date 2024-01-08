from django.db import models
from UserSoliq.models import UsersModel
# Create your models here

class UserCard(models.Model):
    card_holder = models.OneToOneField(UsersModel, on_delete=models.CASCADE)
    expired_date = models.DateField()
    card_number = models.CharField(max_length=16,default="8600",unique=True)
    money = models.IntegerField(default=0)

    def __str__(self):
        return self.card_holder