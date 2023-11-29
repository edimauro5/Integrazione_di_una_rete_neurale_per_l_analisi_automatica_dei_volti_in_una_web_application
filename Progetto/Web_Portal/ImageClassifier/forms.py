from django.core.validators import EMPTY_VALUES
from django.forms.models import ModelChoiceField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Classificazione, Immagine, Rete_Neurale, Valorizzazione
from django.apps import apps


class AccountForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].__init__(widget=forms.TextInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'Nome', 'id': 'nome', 'onchange': 'controlla(this)', 'onkeydown': 'return nonumber(event)'}))
        self.fields['last_name'].__init__(widget=forms.TextInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'Cognome', 'id': 'cognome', 'onchange': 'controlla(this)', 'onkeydown': 'return nonumber(event)'}))
        self.fields['email'].__init__(widget=forms.EmailInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'E-mail', 'id': 'email', 'onchange': 'checkmail(this)'}))
        self.fields['username'].__init__(widget=forms.TextInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'Username', 'id': 'username'}))
        self.fields['password1'].__init__(widget=forms.PasswordInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'Password', 'id': 'password1', 'onkeyup': 'checkpass(this)', 'onchange': 'pass(this)'}))
        self.fields['password2'].__init__(widget=forms.PasswordInput(
            attrs={'class': 'in rounded-3 form-control', 'placeholder': 'Conferma Password', 'id': 'password2'}))


class ImmagineForm(forms.ModelForm):
    class Meta:
        model = Immagine
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*', 'value': 'Carica Immagine', 'onchange': 'readURL(this)', 'style': 'opacity: 0; width: 100px; position: absolute; top: -31px; left: calc(50% - 50px); z-index: -1;'}),
        }


class ValorizzazioneNumberForm(forms.ModelForm):
    class Meta:
        model = Valorizzazione
        fields = ('valore_v',)

    def __init__(self, categoria, *args, **kwargs):
        tmp = Categoria.objects.get(nome=str(categoria))
        super(ValorizzazioneNumberForm, self).__init__(*args, **kwargs)
        self.fields['valore_v'].__init__(widget=forms.NumberInput(
            attrs={'class': 'form-control w-100', 'placeholder': '0 - ' + str(tmp.int_max), 'min': '0', 'max': tmp.int_max, 'step': '1'}))


class ValorizzazioneSelectForm(forms.ModelForm):
    class Meta:
        model = Valorizzazione
        fields = ('valore_v',)

    def __init__(self, categoria, *args, **kwargs):
        tmp = apps.get_model('ImageClassifier', str(categoria))
        super(ValorizzazioneSelectForm, self).__init__(*args, **kwargs)
        self.fields['valore_v'] = ModelChoiceField(
            queryset=tmp.objects.all(), empty_label="--Seleziona--")
        self.fields['valore_v'].widget.attrs['class'] = 'form-select'
        self.fields['valore_v'].widget.attrs['aria-label'] = 'Default select example'


class ValorizzazioneRadioForm(forms.ModelForm):
    class Meta:
        model = Valorizzazione
        fields = ('valore_v',)

    def __init__(self, categoria, *args, **kwargs):
        tmp = apps.get_model('ImageClassifier', str(categoria))
        tmp1 = tmp.objects.all()
        opz = []
        for i in tmp1:
            opz.append((i.opzione, i.opzione))
        super(ValorizzazioneRadioForm, self).__init__(*args, **kwargs)
        self.fields['valore_v'].__init__(widget=forms.RadioSelect(
            attrs={'class': 'my-auto'}, choices=opz))


class ClassificazioneForm(forms.ModelForm):
    class Meta:
        model = Classificazione
        fields = ('rete_neurale', 'threshold',)

    def __init__(self, macro, *args, **kwargs):
        super(ClassificazioneForm, self).__init__(*args, **kwargs)
        self.fields['rete_neurale'] = ModelChoiceField(
            queryset=Rete_Neurale.objects.all().filter(macrocategoria=macro), empty_label="--Seleziona--")
        self.fields['rete_neurale'].widget.attrs['class'] = 'form-select'
        self.fields['rete_neurale'].widget.attrs['aria-label'] = 'Default select example'
        self.fields['threshold'].__init__(widget=forms.NumberInput(
            attrs={'class': 'form-range', 'type': 'range', 'value': '0.4', 'min': '0', 'max': '1', 'step': '0.01', 'oninput':'this.nextElementSibling.value = this.value'}))
