from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import UserProfile, MarathonTeam
from django.contrib.auth.models import User
from seccim_app.models import Lecture
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm


class Register(View):

    def get(self, request):
        return render(
            request,
            'register.html',
            context={},
        )

    def post(self, request):

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            userObj = form.cleaned_data
            email = userObj['email']
            password = userObj['password']

            confirm_password = userObj['confirmPassword']
            gender = request.POST['gender']
            name = request.POST['name']
            age = request.POST['age']
            telephone = request.POST['telephone']
            schooling = request.POST['schooling']
            course = request.POST['course']
            institution = request.POST['institution']
            period = request.POST['period']

            if password != confirm_password:
                error = "As senha são diferentes"
                return render(request, 'register.html', {"error": error})
            elif User.objects.filter(username=email).exists() and not User.is_authenticated:
                error = "Usuario já cadastrado"
                return render(request, 'register.html', {"error": error})
            else:
                try:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.save()

                    profile = UserProfile(user=user)

                    profile.name = name
                    profile.age = age
                    profile.telephone = telephone
                    profile.gender = gender
                    profile.schooling = schooling
                    profile.course = course
                    profile.institution = institution
                    profile.period = period

                    profile.save()

                    login(request, user)
                except:
                    return render(request, 'register.html', {'error': 'Erro ao salvar usuário, possível email já cadastrado.'})

                return render(request, 'index.html', {'register_success': True})
        else:
            required_fileds = []
            for k in list(form.errors.keys()):
                required_fileds.append(k)
            return render(request, 'register.html', {'form_errors': required_fileds})


class UpdateRegister(View):

    def get(self, request):

        user = request.user

        if User.is_authenticated:

            return render(
                request,
                'register.html',
                context={'user': user},
            )

        return HttpResponseRedirect("/")

    def post(self, request):

        if not User.is_authenticated:
            return HttpResponseRedirect("/")

        user = request.user

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            email = userObj['email']
            password = userObj['password']

            confirm_password = userObj['confirmPassword']
            gender = request.POST['gender']
            name = request.POST['name']
            age = request.POST['age']
            telephone = request.POST['telephone']
            schooling = request.POST['schooling']
            course = request.POST['course']
            institution = request.POST['institution']
            period = request.POST['period']

            if password != confirm_password:
                error = 'As senha sao diferentes'
                return render(request, 'register.html', {'error': error})
            elif email != user.email:
                error = 'Email diferente'
                return render(request, 'register.html', {'error': error})
            else:
                user.set_password(password)

                user.save()

                profile = user.profile

                profile.name = name
                profile.age = age
                profile.telephone = telephone
                profile.gender = gender
                profile.schooling = schooling
                profile.course = course
                profile.institution = institution
                profile.period = period

                profile.save()

                login(request, user)

                return HttpResponseRedirect("/")
        else:
            return render(request, 'register.html', {'form': form.errors.keys})


class RegisterTeam(View):

    def get(self, request):

        return render(
            request,
            'register_marathon_team.html',
            context={'user': request.user},
        )

    def post(self, request):
        if not User.is_authenticated:
            return HttpResponseRedirect("/")

        if not request.POST['nick']:
            error = 'Nick do time é obrigatório'
            return render(request, 'register_marathon_team.html', {'error': error})

        profile = request.user.profile

        if not profile.team:

            teams = MarathonTeam.objects.filter()

            if teams.all().count() >= 12:
                error = 'Número de times máximos já foi cadastrado no sistema tratar com os organizadores do evento.'
                return render(request, 'register_marathon_team.html', {'error': error})

            marathon_team = MarathonTeam()

            marathon_team.nick = request.POST['nick']

            marathon_team.save()

            profile.team = marathon_team
        else:
            profile.team.nick = request.POST['nick']

        profile.save()
        return render(request, 'register_marathon_team.html', {'success': "Time salvo"})


class Login(View):

    def get(self, request):

        return render(
            request,
            'login.html',
            context={},
        )

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if email == "":
            return render(request, 'login.html', {'error': "Email é obrigatório"})

        if password == "":
            return render(request, 'login.html', {'error': "Senha é obrigatório"})

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'login.html', {'error': "Usuário não encontrado"})


class Logout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class Payment(View):

    def get(self, request):

        if not request.user.is_staff:
            return HttpResponseRedirect("/")

        users = UserProfile.objects.filter(payed=False)
        return render(request, 'payment.html', context={'users_': users})

    def post(self, request):

        if not request.user.is_staff:
            return HttpResponseRedirect("/")

        users = UserProfile.objects.filter(payed=False)

        for user in users:
            if request.POST.get(user.user.email, False):
                user.payed = True
                user.save()

        return HttpResponseRedirect("/payment")


class Lists(View):

    def get(self, request):

        if not request.user.is_staff:
            return HttpResponseRedirect("/")

        users = UserProfile.objects.filter()
        lectures = Lecture.objects.filter()
        return render(request, 'list_names.html', context={'lectures': lectures, 'users': users, 'lecId': 'all'})

    def post(self, request):

        if not request.user.is_staff:
            return HttpResponseRedirect("/")

        if request.POST['lectures'] == 'all':
            users = UserProfile.objects.filter()
        else:
            users = UserProfile.objects.filter(user__minicourse__lecture=request.POST['lectures'])

        lectures = Lecture.objects.filter()

        return render(request, 'list_names.html', context={'lectures': lectures, 'users': users, 'lecId': request.POST['lectures']})
