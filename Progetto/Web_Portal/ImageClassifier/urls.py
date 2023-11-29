from ImageClassifier.models import Appartenenza, Macrocategoria, Rete_Neurale
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

mc=Macrocategoria.objects.all()
home_img=[]
home_macro=[]
for i in mc:
    home_img.append(str(Appartenenza.objects.all().filter(macrocategoria=str(i)).count()))
    home_macro.append((i.nome, i.descrizione))
rn=Rete_Neurale.objects.all()
home_rn=[]
for i in rn:
    home_rn.append((str(i.nome), str(i.descrizione)))

urlpatterns = [
    path('Homepage', auth_views.LoginView.as_view(
        template_name='ImageClassifier/login.html', extra_context={'home_img':home_img, 'home_rn':home_rn, 'home_macro':home_macro})),
    path('logout', auth_views.LogoutView.as_view()),
    path('Registrazione', views.Registrazione),
    path('Test', views.Test),
]
