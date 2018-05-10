"""projet_inf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path
from sentiments_analysis import views
from django_filters.views import FilterView
#from mysite.search.filters import UserFilter

urlpatterns = [
   path('admin/', admin.site.urls),
	path('index', views.home, name='index'),
	path('', views.accueil, name='accueil'),
	path('liste_tweet', views.liste_tweet, name='liste_tweet'),
	path('carte', views.carte, name='carte'),
	path('graphique', views.graphique, name='graphique'),
	path('page/getData/<type_graphique>/<chrono>/<sentiment>', views.getData),
	path('send_mail', views.sendMail, name='sendMail')
]
#urlpatterns = [
#    url(r'^search/$', FilterView.as_view(filterset_class=UserFilter,
#        template_name='search/user_list.html'), name='search'),
#]
