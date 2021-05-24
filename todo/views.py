from django.shortcuts import render, redirect

from .models import Todo

from .forms import TodoForm


def home_page(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/home_page.html', {'todos': todos})


def add_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/add.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('home')
        except ValueError:
            return render(request, 'todo/add.html',
                          {'form': TodoForm(),
                           'error': 'There is an error in the data. Please try again.'})
