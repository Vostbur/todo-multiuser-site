from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Todo

from .forms import TodoForm


def home_page(request):
    return render(request, 'todo/home.html')


@login_required
def list_todo(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/list.html', {'todos': todos})


@login_required
def completed_todo(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'todo/completed.html', {'todos': todos})


@login_required
def detail_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        return render(request, 'todo/detail.html', {'todo': todo, 'form': TodoForm(instance=todo)})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('list')
        except ValueError:
            return render(request, 'todo/detail.html',
                          {'todo': todo, 'form': form, 'error': 'There is an error in the data. Please try again.'})


@login_required
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('list')


@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('list')


@login_required
def add_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/add.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('list')
        except ValueError:
            return render(request, 'todo/add.html',
                          {'form': TodoForm(),
                           'error': 'There is an error in the data. Please try again.'})
