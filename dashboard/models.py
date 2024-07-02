from django.db import models


class Temperature(models.Model):
    TYPE_CHOICES = (
        ('outside', 'Outside'),
        ('inside', 'Inside'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    temperature = models.FloatField()
    humidity = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.type} - {self.date}"


class ChatMessage(models.Model):
    prompt = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.prompt