from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'users/register.html', {
            'register_form': register_form
        })

    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        # commit False będziemy dokładać inne dane.
        # Ta metoda zapiszę tylko email i hasło.
        user = register_form.save(commit=False)
        user.first_name = user.first_name.capitalize()
        user.last_name = user.last_name.capitalize()
        user.username = user.username.lower()
        user.save()
        return redirect('all_movies')
    else:
        return render(request, 'users/register.html', {'register_form': register_form})
