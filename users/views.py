from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Регістрація нового користувача."""
    if request.method != "POST":
        # Показати порожню форму.
        form = UserCreationForm()
    else:
        # Опрацювати заповнену форму.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            # Авторизувати користувача та спрямувати його на головну сторінку.
            return redirect("uminity_coms:index")

    # Показати порожню форму або недійсну.
    context = {"form": form}
    return render(request, "registration/register.html", context)
