# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Seccim(models.Model):

    version = models.CharField('version', max_length=5, help_text="número romano da edição da seccim")
    is_active = models.BooleanField('is_active', help_text="deve haver somente um ativa")
    start_date = models.DateTimeField('start_date', help_text="inicio do evento", null=True, blank=True)
    end_date = models.DateTimeField('end_date', help_text="fim do evento", null=True, blank=True)
    year = models.IntegerField('year', help_text="ano")
    mini_course_vacancies = models.IntegerField(default=20)

    def __str__(self):
        return 'Seccim' + self.version


class Speaker(models.Model):

    name = models.CharField(max_length=50, help_text="nome do autor.")
    origin = models.CharField(max_length=50, blank=True, null=True, help_text="Empresa ou instituição do palestrante.")

    twitter = models.CharField(max_length=50, blank=True, null=True, help_text="link do twitter.")
    facebook = models.CharField(max_length=50, blank=True, null=True, help_text="link do facebook.")
    linkedin = models.CharField(max_length=50, blank=True, null=True, help_text="link do linkedin.")
    is_male = models.BooleanField('is_male', default=True)

    photo = models.ImageField(blank=True, null=True)
    car_plate = models.CharField(max_length=8, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(max_length=1000, help_text="Descriçao breve do palestrante")
    seccim = models.ForeignKey(Seccim, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lecture(models.Model):

    title = models.CharField('title', max_length=100, help_text="Nome da palestra.")
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    date = models.DateTimeField('lecture_date', unique=True)
    equipment = models.CharField('equipments', max_length=100, null=True, blank=True)
    description = models.TextField('description', max_length=1000, help_text="Descrição da palestra", default="")
    seccim = models.ForeignKey(Seccim, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class MiniCourse(models.Model):

    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    enrolled = models.ManyToManyField(User, blank=True, default=None)
    vacancies = models.IntegerField('vacancies')

    def __str__(self):
        return self.lecture.title
