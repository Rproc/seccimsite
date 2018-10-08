from django.conf.urls import url
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from seccim_app.views import *
from user_profile.views import Register, UpdateRegister, Lists
from user_profile.views import Login, Logout, RegisterTeam, Payment

handler404 = 'seccim_app.views.ErrorHandler404'
handler500 = 'seccim_app.views.ErrorHandler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^index/$', Index.as_view()),
    url(r'^signup/$', Register.as_view()),
    url(r'^register/$', UpdateRegister.as_view()),
    url(r'^marathon/$', RegisterTeam.as_view()),
    url(r'^marathon_team/$', RegisterTeam.as_view()),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^register_course/$', RegisterCourse.as_view()),
    url(r'^out_course/$', ExitCourse.as_view()),
    url(r'^payment/$', Payment.as_view()),
    url(r'^lists/$', Lists.as_view()),
    url(r'^certificates/$', TemplateView.as_view(template_name='comming_soon.html'), name='certificates'),

    #reset password
    # url(r'^reset_password/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #reset_password

    url(r'^$', RedirectView.as_view(url='/index/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
