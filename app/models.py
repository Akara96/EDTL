from django.db import models
from django.contrib.auth.models import User

class Munisipiu(models.Model):
    munisipiu = models.CharField(max_length=25, null=True, blank=True)
    kodigu    = models.CharField(max_length=25, null=True, blank=True)
    area      = models.TextField(null=True, blank=True)
    inline_color = models.CharField(max_length=7, null=True, blank=True)  # Hex color code
    outline_color = models.CharField(max_length=7, null=True, blank=True)  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.munisipiu


class Postu(models.Model):
    postu = models.CharField(max_length=15, null=True, blank=True)
    munisipiu = models.ForeignKey(Munisipiu, on_delete=models.CASCADE, related_name='postus')

    def __str__(self):
        return self.postu


class Suku(models.Model):
    suku = models.CharField(max_length=25, null=True, blank=True)
    postu = models.ForeignKey(Postu, on_delete=models.CASCADE, null=True, blank=True, related_name='sukus')

    def __str__(self):
        return self.suku


class Aldeia(models.Model):
    naran_aldeia = models.CharField(max_length=30, null=True, blank=True)
    suku = models.ForeignKey(Suku, on_delete=models.CASCADE, null=True, blank=True, related_name='aldeias')

    def __str__(self):
        return self.naran_aldeia


class Tekniku(models.Model):
    # id = models.CharField(primary_key=True, max_length=10, null=False, blank=True)
    id_tekniku = models.CharField(max_length=10, null=True, blank=True)
    naran = models.CharField(max_length=50, null=True, blank=True)
    enderesu = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    no_tlf = models.CharField(max_length=8, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.naran


class Feeder(models.Model):
    munisipiu    = models.ForeignKey(Munisipiu, on_delete=models.CASCADE, null=True, blank=True)
    naran_feeder = models.CharField(max_length=20, null=True, blank=True)
    marka        = models.CharField(max_length=40, null=True, blank=True)
    deskrisaun_zona = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.naran_feeder

class KordinatFeeder(models.Model):
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True, blank=True)
    kordinat = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Kordinat for {self.feeder}"


class Trafo(models.Model):
    kordinat = models.TextField()
    zona = models.CharField(max_length=20, null=True, blank=True)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Trafo {self.id}"


class Cliente(models.Model):
    KATEGORI_KLIENTE_CHOICES = [
        ('rezidensial', 'Rezidensial'),
        ('komersial', 'Komersial'),
        ('sosial', 'Sosial'),
        ('governu', 'Governu'),
        ('agensia internasional', 'Agensia Internasional'),
    ]

    naran = models.CharField(max_length=50, null=True, blank=True)
    id_identidade = models.CharField(max_length=11, null=True, blank=True)
    naran_kompanhia = models.CharField(max_length=30, blank=True)
    kategoria_kliente = models.CharField(max_length=25, choices=KATEGORI_KLIENTE_CHOICES)
    hela_fatin = models.CharField(max_length=25, null=True, blank=True)
    # kordinat = models.CharField(max_length=100, null=True, blank=True)
    no_tlf = models.CharField(max_length=12, null=True, blank=True)
    aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE, null=True, blank=True)
    tekniku = models.ForeignKey(Tekniku, on_delete=models.SET_NULL, null=True)
    data_rejistu = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.naran


class RejistuKontadorFoun(models.Model):
    naran_kliente = models.CharField(max_length=30, null=True, blank=True)
    numeru = models.CharField(max_length=8, null=True, blank=True)
    email = models.EmailField(max_length=60, null=True, blank=True)
    aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE, null=True, blank=True)
    data_pedidu = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.naran_kliente


class Selu(models.Model):
    montante = models.FloatField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente} - {self.montante}"


class Survey(models.Model):
    TIPO_LIGASAUN_CHOICES = [
        ('monofasico', 'Monofasico'),
        ('trifasico', 'Trifasico'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    tipu_ligasaun = models.CharField(max_length=10, choices=TIPO_LIGASAUN_CHOICES, null=True, blank=True)
    feeder = models.CharField(max_length=3, null=True, blank=True)
    nu_trafo = models.CharField(max_length=5, null=True, blank=True)
    data_survey = models.DateField(null=True, blank=True)
    deskrisaun_instalasaun = models.TextField(null=True, blank=True)
    tekniku = models.ForeignKey(Tekniku, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def kalkulasaun(self):
        if self.tipu_ligasaun == 'trifasico':
            return 315.00
        elif self.tipu_ligasaun == 'monofasico':
            return 35.00
        else:
            return 0.00

    def __str__(self):
        return f"Survey {self.id}"


class Imajen(models.Model):
    foto = models.ImageField(upload_to='imajen/', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Imajen {self.id}"


class Contador(models.Model):
    PHASE_CHOICES = [
        ('mono phase', 'Mono Phase'),
        ('three phase', 'Three Phase'),
    ]

    LIGASAUN_ARDE_CHOICES = [
        ('iha', 'Iha'),
        ('laiha', 'Laiha'),
    ]

    nu_kontador = models.CharField(max_length=11, null=True, blank=True)
    phase = models.CharField(max_length=15, choices=PHASE_CHOICES, null=True, blank=True)
    disjuntor_jeral = models.IntegerField(null=True, blank=True)
    medida_kabu = models.CharField(max_length=10, null=True, blank=True)
    numeru_trafo = models.CharField(max_length=10, null=True, blank=True)
    numeru_pole = models.CharField(max_length=10, null=True, blank=True)
    konta_tuan = models.CharField(max_length=11, null=True, blank=True)
    ligasaun_arde = models.CharField(max_length=10, choices=LIGASAUN_ARDE_CHOICES, null=True, blank=True)
    kordinat = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    trafo = models.ForeignKey(Trafo, on_delete=models.CASCADE, null=True, blank=True)
    tekniku = models.ForeignKey(Tekniku, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Kontador {self.nu_kontador}"


class Keixa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente (Menunggu)'),
        ('prosesu', 'Iha Prosesu (Sedang Dikerjakan)'),
        ('remata', 'Remata (Selesai)'),
    ]

    KATEGORIA_CHOICES = [
        ('mate_lampu', 'Mati Lampu (Blackout)'),
        ('trafo_aat', 'Trafo Bermasalah'),
        ('kontador_aat', 'Meteran Rusak'),
        ('seluk', 'Lain-lain'),
    ]

    kodigu_keixa = models.CharField(max_length=20, null=True, blank=True, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    kategoria = models.CharField(max_length=20, choices=KATEGORIA_CHOICES, null=True, blank=True)
    deskrisaun = models.TextField(null=True, blank=True)
    data_keixa = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    tekniku = models.ForeignKey(Tekniku, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='keixa/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Keixa {self.kodigu_keixa} - {self.cliente}"