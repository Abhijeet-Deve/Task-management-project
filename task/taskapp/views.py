from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime

# Home Page - List All Tasks
def home(request):
    # Get the 'status' filter from query parameters (if any)
    status_filter = request.GET.get('status', None)
    
    if status_filter:
        tasks = Task.objects.filter(status=status_filter)
    else:
        tasks = Task.objects.all()
    
    return render(request, 'home.html', {'tasks': tasks, 'status_filter': status_filter})


# Add Task
def add_task(request):
    if request.method == "POST":
        description = request.POST['description']
        deadline = request.POST['deadline']
        Task.objects.create(description=description, deadline=deadline)
        return redirect(reverse('home'))
    return render(request, 'add_task.html')

# Update Task
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == "POST":
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        
        # Handle deadline as text
        deadline = request.POST.get('deadline')
        if deadline:  # Only update if a text value is provided
            task.deadline = deadline  # Save as text string

        task.save()
        return redirect(reverse('home'))

    return render(request, 'update_task.html', {'task': task})
# Delete Task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect(reverse('home'))
    return render(request, 'delete_task.html', {'task': task})
