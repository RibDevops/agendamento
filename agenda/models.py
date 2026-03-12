from django.db import models


class AgendaEvento(models.Model):

    data = models.DateField()

    dia = models.CharField(
        max_length=5
    )

    titulo = models.CharField(
        max_length=255
    )

    tipo = models.CharField(
        max_length=50
    )

    datas = models.CharField(
        max_length=100
    )

    descricao = models.TextField()

    hash = models.CharField(
        max_length=64,
        unique=True
    )

    enviado_whatsapp = models.BooleanField(
        default=False
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.data} - {self.titulo}"