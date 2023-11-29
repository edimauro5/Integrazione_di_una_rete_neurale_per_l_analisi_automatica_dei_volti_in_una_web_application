from django.contrib import admin
from .models import Categoria, Classificazione, Composizione, Macrocategoria, Immagine, Appartenenza, Prestazione, Rete_Neurale, Valorizzazione, Genere, Etnia, Emozione

# Register your models here.

admin.site.register(Immagine)
admin.site.register(Macrocategoria)
admin.site.register(Appartenenza)
admin.site.register(Rete_Neurale)
admin.site.register(Categoria)
admin.site.register(Classificazione)
admin.site.register(Valorizzazione)
admin.site.register(Composizione)
admin.site.register(Prestazione)
admin.site.register(Genere)
admin.site.register(Etnia)
admin.site.register(Emozione)
