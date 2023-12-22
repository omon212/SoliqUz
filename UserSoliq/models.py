from django.db import models

# Create your models here.


class UsersModel(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    tel_number = models.CharField(max_length=9,unique=True)
    PS_seriya = models.CharField(max_length=2)
    PS_raqam = models.CharField(max_length=7)
    JSHHIR = models.CharField(max_length=14)
    day_of_birthday = models.DateField()

    def __str__(self):
        return self.name




