from django.db import models
from django.contrib.auth.models import User


class MarathonTeam(models.Model):

    nick = models.CharField('nick', max_length=30)


class UserProfile(models.Model):

    GENDER_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
    )

    SCHOOLING_CHOICES = (
        ("0", "0"),
        ("1", "Ensino Fundamental"),
        ("2", "Ensino Medio"),
        ("3", "Superior incompleto"),
        ("4", "Superior completo"),
        ("5", "Pos-graduado"),
        ("6", "Mestrado"),
        ("7", "Doutorado"),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    name = models.CharField('name', max_length=100)
    age = models.IntegerField('age')
    telephone = models.CharField('telephone', max_length=15)
    gender = models.CharField('gender', max_length=9, choices=GENDER_CHOICES, default="M")
    schooling = models.CharField('schooling', max_length=1, choices=SCHOOLING_CHOICES, default="0")
    course = models.CharField('course', max_length=50)
    institution = models.CharField('institution', max_length=50)
    period = models.CharField('period', max_length=20)
    payed = models.BooleanField('payed', default=False)

    team = models.ForeignKey(MarathonTeam, null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['name', 'schooling']

    def __unicode__(self):
        return self.user.username

    def getFirstName(self):
        return self.name.split(' ')[0]
