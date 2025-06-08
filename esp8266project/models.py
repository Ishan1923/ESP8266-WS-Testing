from django.db import models

class sensordata(models.Model):
    text = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"{self.timestamp} : {self.text}"