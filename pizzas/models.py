from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pizza(models.Model):
    """A pizza the pizzeria offers"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Topping(models.Model):
    """Toppings for pizzas."""
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self):
        if len(self.name) > 50:
            return f'{self.name[:50]}...'
        else:
            return self.name            

