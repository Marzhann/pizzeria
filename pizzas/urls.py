"""Defines URL patterns for the pizzas"""

from django.urls import path
from . import views

app_name = 'pizzas'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Other pages
    path('pizzas/', views.pizzas, name='pizzas'),
    path('pizzas/<int:pizza_id>/', views.pizza, name='pizza'),
    path('new_pizza/', views.new_pizza, name='new_pizza'),
    path('add_topping/<int:pizza_id>', views.add_topping, name='add_topping'),
    path('edit_topping/<int:topping_id>', views.edit_topping, name='edit_topping'),
]