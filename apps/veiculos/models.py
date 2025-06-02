from django.db import models


class Veiculo(models.Model):
    class Marca(models.TextChoices):
        CHEVROLET = 'CHEVROLET', 'Chevrolet'
        FIAT = 'FIAT', 'Fiat'
        FORD = 'FORD', 'Ford'
        VOLKSWAGEN = 'VOLKSWAGEN', 'Volkswagen'
        RENAULT = 'RENAULT', 'Renault'
        HONDA = 'HONDA', 'Honda'
        TOYOTA = 'TOYOTA', 'Toyota'
        HYUNDAI = 'HYUNDAI', 'Hyundai'
        NISSAN = 'NISSAN', 'Nissan'
        PEUGEOT = 'PEUGEOT', 'Peugeot'
        CITROEN = 'CITROEN', 'Citroën'
        JEEP = 'JEEP', 'Jeep'
        MITSUBISHI = 'MITSUBISHI', 'Mitsubishi'
        KIA = 'KIA', 'Kia'
    veiculo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, choices=Marca.choices)
    ano = models.IntegerField()
    descricao = models.TextField()
    vendido = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} {self.veiculo} ({self.ano})"