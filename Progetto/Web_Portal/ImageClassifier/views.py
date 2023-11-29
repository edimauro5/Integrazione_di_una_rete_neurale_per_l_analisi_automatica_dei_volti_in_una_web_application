from ImageClassifier.models import Appartenenza, Categoria, Classificazione, Composizione, Immagine, Macrocategoria, Prestazione, Rete_Neurale, Valorizzazione
from .forms import AccountForm, ClassificazioneForm, ImmagineForm, ValorizzazioneNumberForm, ValorizzazioneRadioForm, ValorizzazioneSelectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from Face_Bio.face_bio import *
from Face_Bio.face_bio import init_net as init_bio
from Count_Vehicles.count_vehicles import *
from Count_People.count_people import *
from Count_Faces.count_faces import *
from django.db import transaction
import datetime


# Create your views here.


def Homepage(request):
    return render(request, 'ImageClassifier/login.html')


def Registrazione(request):
    form = AccountForm()
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            login(request, account)
            return redirect('/ImageClassifier/Homepage')
    return render(request, 'ImageClassifier/Registrazione.html', {'form': form})


@login_required(login_url='/ImageClassifier/Homepage', redirect_field_name='/ImageClassifier/Homepage')
def Test(request):
    if (request.method == 'GET') and (request.GET.get('macro') != None):
        macro = request.GET.get('macro').replace('_', ' ')
        comp_set = Composizione.objects.all().filter(macrocategoria=macro)
        form_set = []
        form1 = ImmagineForm()
        for i in comp_set:
            tmp = Categoria.objects.get(nome=i.categoria)
            a = 'Valorizzazione'+tmp.tipo+'Form'
            form_set.append((i.categoria, globals()[a](i.categoria)))
        form3 = ClassificazioneForm(macro)
        return render(request, 'ImageClassifier/Test.html', {'form1': form1, 'macro': macro, 'form_set': form_set, 'form3': form3})

    if request.method == 'POST':
        macro = request.POST.get("macrocategoria", "")
        comp_set = Composizione.objects.all().filter(macrocategoria=macro)
        form_set = []
        form1 = ImmagineForm(request.POST, request.FILES)
        form1_valid = form1.is_valid()

        form_scroll_valid = True
        for count, i in enumerate(comp_set):
            tmp = Categoria.objects.get(nome=i.categoria)
            a = 'Valorizzazione'+tmp.tipo+'Form'
            tmp_form = globals()[a](i.categoria, {'valore_v': str(
                request.POST.getlist('valore_v')[count])})
            if tmp_form.is_valid() == False:
                form_scroll_valid = False
            else:
                form_set.append(
                    (i.categoria, str(request.POST.getlist('valore_v')[count])))
        form_value = []
        form3 = ClassificazioneForm(macro, request.POST)
        form3_valid = form3.is_valid()
        img = Immagine.objects.all().filter(image=form1.instance)
        if(bool(img)):
            img_tmp = img[0]
        else:
            img_tmp = form1.instance
        mac = Appartenenza.objects.all().filter(macrocategoria=macro, immagine=img_tmp)
        ris = []
        with transaction.atomic():
            if form1_valid:
                form1.save()
            if bool(mac) == False:
                tmp1 = Appartenenza(macrocategoria=Macrocategoria(
                    str(macro)), immagine=img_tmp)
                tmp1.save()
            if form_scroll_valid and form3_valid:
                rn = form3.cleaned_data['rete_neurale']
                th = form3.cleaned_data['threshold']
                if str(rn) == 'Face Bio':
                    nn, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier, shape, gender_labels, ethnicity_labels, emotion_labels = init_bio(
                        'Face_Bio/detector.pb', 'Face_Bio/gender.hdf5', 'Face_Bio/age.hdf5', 'Face_Bio/ethnicity.hdf5', 'Face_Bio/emotion.hdf5')
                    ris = classify_faces(nn, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier,
                                         'Media/' + str(img_tmp), th, shape, gender_labels, ethnicity_labels, emotion_labels)
                else:
                    nn = init_net(str(rn).replace(
                        ' ', '_') + '/model-final.pb')
                    ris.append(globals()[str(rn).replace(' ', '_').lower()](
                        nn, 'Media/'+str(img_tmp), th))
                for count, f in enumerate(form_set):
                    if(bool(Valorizzazione.objects.all().filter(categoria=Categoria(f[0]), immagine=img_tmp)) == False):
                        tmp2 = Valorizzazione(categoria=Categoria(f[0]), immagine=img_tmp, valore_v=str(
                            request.POST.getlist('valore_v')[count]))
                        tmp2.save()
                    tmp3 = Classificazione(data=datetime.date.today(), rete_neurale=rn, categoria=Categoria(
                        f[0]), valore_rn=ris[count], immagine=img_tmp, threshold=th)
                    tmp3.save()
                    form_value.append((f, ris[count], Prestazione.objects.get(rete_neurale=rn, categoria=Categoria(f[0])).valore_p, Categoria.objects.get(nome=f[0]).tipo))
                nclass=Classificazione.objects.all().filter(rete_neurale=rn).count()
                return render(request, 'ImageClassifier/Result.html', {'form1': img_tmp, 'macro': macro, 'form_value': form_value, 'rn': rn, 'th': th, 'nclass': nclass})
            else:
                print("quello che hai caricato non va bene")

    return redirect('/ImageClassifier/Homepage')
