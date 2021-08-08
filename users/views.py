from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        # This is a POST request. process data
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and redirect to the home page
            login(request, new_user)
            return redirect('pizzas:index')
            
    context = {'form': form}
    return render(request, 'registration/register.html', context)