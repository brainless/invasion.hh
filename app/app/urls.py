"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from surfers.views import RegistrationView, LoginView, ProfileView, DashView
from events.views import SelectActivitiesView, EventParticipationView, ParticipantsView


urlpatterns = [
    url(r'^app/admin/', admin.site.urls),

    url(r'^app/register/', RegistrationView.as_view()),
    url(r'^app/login/', LoginView.as_view()),
    url(r'^app/logout/$', LogoutView.as_view(next_page='/')),

    url(r'^app/profile/', ProfileView.as_view()),
    url(r'^app/dash/$', DashView.as_view()),

    url(r'^app/select-activities/', SelectActivitiesView.as_view(), name='current_activities'),
    url(r'^app/participation/', EventParticipationView.as_view(), name='current_participation'),

    url(r'^app/(?P<pk>[0-9]+)/participants/', ParticipantsView.as_view())
]
