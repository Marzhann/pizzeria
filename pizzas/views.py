from django.shortcuts import render, redirect
from .models import Pizza, Topping
from .forms import PizzaForm, ToppingForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    """The home page for the pizzeria"""
    return render(request, 'pizzas/index.html')

@login_required
def pizzas(request):
    """Shows list of all pizzas"""
    pizzas = Pizza.objects.filter(owner=request.user).order_by('name')
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)

@login_required
def pizza(request, pizza_id):
    """Shows toppings for the requested pizza"""
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.order_by('name')
    # Check is the user owner of this object
    check_the_owner(request, pizza)
    
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/pizza.html', context)

@login_required
def new_pizza(request):
    """Add new pizza to a menu"""
    if request.method != 'POST':
        # No data submitted. Create a blank form
        form = PizzaForm()
    else:
        # POST data submitted. process data
        form = PizzaForm(data=request.POST)
        # check if submitted form is valid
        if form.is_valid():
            new_pizza = form.save(commit=False)
            new_pizza.owner = request.user
            new_pizza.save()
            return redirect('pizzas:pizzas')

    content = {'form':form}
    return render(request, 'pizzas/new_pizza.html', content)

@login_required
def add_topping(request, pizza_id):
    """Add toppings to the pizza"""
    pizza = Pizza.objects.get(id=pizza_id)
    # Check is the user owner of this object
    check_the_owner(request, pizza)

    if request.method != 'POST':
        form = ToppingForm()
    else:
        form = ToppingForm(data=request.POST)
        if form.is_valid():
            new_topping = form.save(commit=False)
            new_topping.pizza = pizza
            new_topping.save()
            return redirect('pizzas:pizza', pizza_id = pizza_id)
    context = {'pizza': pizza, 'form': form}
    return render(request, 'pizzas/add_topping.html', context)

@login_required
def edit_topping(request, topping_id):
    """Edit existing topping"""
    topping = Topping.objects.get(id=topping_id)
    pizza = topping.pizza
    # Check is the user owner of this object
    check_the_owner(request, pizza)

    if request.method != 'POST':
        form = ToppingForm(instance=topping)
    else:
        form = ToppingForm(instance=topping, data=request.POST)
        if form.is_valid():
            form.save()             
            return redirect('pizzas:pizza', pizza_id = pizza.id)
    
    context = {'form': form, 'topping': topping, 'pizza': pizza}
    return render(request, 'pizzas/edit_topping.html', context)

def check_the_owner(request, pizza):
    if request.user != pizza.owner:
        raise Http404

