from django.db import models
from UserSoliq.models import UsersModel
class CheckModel(models.Model):
    name = models.ForeignKey(UsersModel,on_delete=models.CASCADE)
    money = models.IntegerField()
    where = models.CharField(max_length=255)
    fiskal_raqam = models.CharField(max_length=14,unique=True)
    CHOISES = (
        ("UZ","UZ"),
        ("VG", "VG"),
        ("NA", "NA"),
        ("ZZ", "ZZ"),
        ("EP", "EP"),
        ("EZ", "EZ"),
        ("LG", "LG"),
        ("ET", "ET"),
    )
    fiskal_seriya = models.CharField(choices=CHOISES,max_length=2)

    def __str__(self):
        return self.fiskal_raqam
