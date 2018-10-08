from django.shortcuts import render
from django.views.generic import View
from .models import Lecture, Speaker, Seccim, MiniCourse
from user_profile.models import UserProfile, MarathonTeam
from django.contrib import admin
import random
from django.http import HttpResponseRedirect
from django.utils import timezone


admin.site.register(Speaker)
admin.site.register(Lecture)
admin.site.register(UserProfile)
admin.site.register(Seccim)
admin.site.register(MiniCourse)
admin.site.register(MarathonTeam)


class ErrorHandler404(View):

    def get(self, request):
        response = render(request, '404.html', {})
        response.status_code = 404
        return response

    def post(self, request):
        response = render(request, '404.html', {})
        response.status_code = 404
        return response


class ErrorHandler500(View):

    def get(self, request):
        response = render(request, '500.html', {})
        response.status_code = 500
        return response

    def post(self, request):
        response = render(request, '500.html', {})
        response.status_code = 500
        return response


class Index(View):

    def get(self, request):

        seccim = Seccim.objects.filter(is_active=True)[0]

        values = {'version': seccim.version, 'start_date': seccim.start_date, 'end_date': seccim.end_date}

        days = [day for day in range(seccim.start_date.day, seccim.end_date.day)]

        lectures = Lecture.objects.filter(seccim=seccim, minicourse__isnull=True).order_by('date')
        speakers = Speaker.objects.filter(seccim=seccim)
        mini_course = MiniCourse.objects.filter(lecture__seccim=seccim)

        if request.user.is_authenticated:
            user_mini_courses = MiniCourse.objects.filter(enrolled=request.user)
        else:
            user_mini_courses = None

        photos_indexes = random.sample(range(1, 18), 15)

        for mini in mini_course:

            if user_mini_courses is not None and user_mini_courses.count() < 2 and \
                            request.user not in mini.enrolled.all() and \
                    (request.user.is_superuser or request.user.profile.payed):
                mini.showButton = True
            else:
                mini.showButton = False

            if mini.vacancies <= mini.enrolled.all().count():
                mini.places = 0
            else:
                mini.places = mini.vacancies - mini.enrolled.all().count()

        values['lectures'] = lectures
        values['speakers'] = speakers
        values['mini_courses'] = mini_course
        values['days'] = days
        values['photos_indexes'] = photos_indexes
       
        return render(
            request,
            'index.html',
            context=values,
        )


class RegisterCourse(View):

    def post(self, request):
        lecture_id = request.POST['course_id']

        mini_course = MiniCourse.objects.filter(lecture_id=lecture_id)[0]
        user_mini_courses = MiniCourse.objects.filter(enrolled=request.user)

        if mini_course.lecture.date > timezone.now() and mini_course.enrolled.all().count() < mini_course.vacancies and user_mini_courses.count() < 2:
            mini_course.enrolled.add(request.user)

            return HttpResponseRedirect("/")
        else:
            return render(request, 'index.html', {'error': "mini_course"})


class ExitCourse(View):

    def post(self, request):
        lecture_id = request.POST['course_id']

        mini_course = MiniCourse.objects.filter(lecture_id=lecture_id)[0]

        if mini_course.lecture.date > timezone.now():
            mini_course.enrolled.remove(request.user)

        return HttpResponseRedirect("/")
