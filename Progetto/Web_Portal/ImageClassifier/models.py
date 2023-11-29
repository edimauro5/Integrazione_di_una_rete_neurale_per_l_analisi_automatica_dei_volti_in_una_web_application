from django.db import models

# Create your models here.


class Immagine(models.Model):
    class Meta:
        db_table= "immagine"
    codice = models.AutoField(primary_key=True)
    image = models.ImageField(unique=True)

    def __str__(self):
        return str(self.image)


class Macrocategoria(models.Model):
    class Meta:
        db_table= "macrocategoria"
    nome = models.CharField(max_length=30, primary_key=True)
    descrizione = models.CharField(max_length=500)

    def __str__(self):
        return self.nome


class Appartenenza(models.Model):
    class Meta:
        db_table= "appartenenza"
        unique_together = (('macrocategoria', 'immagine'),)
    macrocategoria = models.ForeignKey(
        to='Macrocategoria', on_delete=models.CASCADE)
    immagine = models.ForeignKey(to='Immagine', on_delete=models.CASCADE)

    def __str__(self):
        return str(str(self.macrocategoria) + " - " + str(self.immagine))


class Rete_Neurale(models.Model):
    class Meta:
        db_table= "rete_neurale"
    codice = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, unique=True)
    ultimo_ripristino = models.DateField()
    descrizione = models.CharField(max_length=500)
    macrocategoria = models.ForeignKey(
        to='Macrocategoria', on_delete=models.RESTRICT)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    class Meta:
        db_table= "categoria"
    nome = models.CharField(max_length=30, primary_key=True)
    tipo = models.CharField(max_length=30)
    int_max = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Classificazione(models.Model):
    class Meta:
        db_table= "classificazione"
    data = models.DateField()
    rete_neurale = models.ForeignKey(
        to='Rete_Neurale', on_delete=models.RESTRICT)
    categoria = models.ForeignKey(to='Categoria', on_delete=models.RESTRICT)
    immagine = models.ForeignKey(to='Immagine', on_delete=models.RESTRICT)
    valore_rn = models.CharField(max_length=30)
    threshold = models.DecimalField(
        max_digits=3, decimal_places=2)

    def __str__(self):
        return str(str(self.rete_neurale) + " - " + str(self.categoria) + " - " + str(self.immagine))


class Valorizzazione(models.Model):
    class Meta:
        db_table= "valorizzazione"
        unique_together = (('categoria', 'immagine'),)
    categoria = models.ForeignKey(to='Categoria', on_delete=models.RESTRICT)
    immagine = models.ForeignKey(to='Immagine', on_delete=models.CASCADE)
    valore_v = models.CharField(max_length=30)

    def __str__(self):
        return str(str(self.categoria) + " - " + str(self.immagine))


class Composizione(models.Model):
    class Meta:
        db_table= "composizione"
        unique_together = (('macrocategoria', 'categoria'),)
    macrocategoria = models.ForeignKey(
        to='Macrocategoria', on_delete=models.CASCADE)
    categoria = models.ForeignKey(to='Categoria', on_delete=models.RESTRICT)

    def __str__(self):
        return str(str(self.macrocategoria) + " - " + str(self.categoria))


class Prestazione(models.Model):
    class Meta:
        db_table= "prestazione"
        unique_together = (('rete_neurale', 'categoria'),)
    rete_neurale = models.ForeignKey(
        to='Rete_Neurale', on_delete=models.CASCADE)
    categoria = models.ForeignKey(to='Categoria', on_delete=models.RESTRICT)
    valore_p = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(str(self.rete_neurale) + " - " + str(self.categoria))


class Genere(models.Model):
    class Meta:
        db_table= "genere"
    opzione = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.opzione


class Etnia(models.Model):
    class Meta:
        db_table= "etnia"
    opzione = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.opzione


class Emozione(models.Model):
    class Meta:
        db_table= "emozione"
    opzione = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.opzione
