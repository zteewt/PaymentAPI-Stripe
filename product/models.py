from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    desсription = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_price_in_dollars(self):
        return f"${self.price / 100:.2f}"