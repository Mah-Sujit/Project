```python
# Title: Simple To-Do List App using Django with Error Handling

# Ensure you have Django installed. If not, install it using:
# pip install django

# Step 1: Set up Django Project and App
# In your terminal, navigate to your desired directory and run the following commands:
# django-admin startproject todolist_project
# cd todolist_project
# python manage.py startapp tasks

# Step 2: Define models in tasks/models.py

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the task title.")
    description = models.TextField(blank=True, help_text="Optional: Enter task description.")
    completed = models.BooleanField(default=False, help_text="Mark as completed if the task is done.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the task was last updated.")
    
    def __str__(self):
        return self.title

# Step 3: Register the model in tasks/admin.py

from django.contrib import admin
from .models import Task

admin.site.register(Task)

# Step 4: Configure the app in todolist_project/settings.py by adding 'tasks' to INSTALLED_APPS

INSTALLED_APPS = [
    ...
    'tasks',
    ...
]

# Step 5: Create migrations and apply them to set up the database

# Run the following commands in the terminal:
# python manage.py makemigrations
# python manage.py migrate

# Step 6: Add views to handle task creation, display, and error handling in tasks/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Task
from .forms import TaskForm

def index(request):
    try:
        tasks = Task.objects.all()
    except Task.DoesNotExist:
        tasks = []
    return render(request, 'tasks/index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        else:
            return render(request, 'tasks/add_task.html', {'form': form})
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def task_detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task not found")
    return render(request, 'tasks/task_detail.html', {'task': task})

# Step 7: Create forms for task entry in tasks/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

# Step 8: Set up URLs for the app in tasks/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]

# Step 9: Include app URLs into the project URLs in todolist_project/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
]

# Step 10: Prepare basic templates (assuming you have set up templates directory settings)

# Create the following HTML files in a directory named `templates` within the `tasks` app:
# - index.html
# - add_task.html
# - task_detail.html

# Sample content for index.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h1>Task List</h1>
    <a href="{% url 'add_task' %}">Add New Task</a>
    <ul>
        {% for task in tasks %}
            <li>
                <a href="{% url 'task_detail' task.id %}">{{ task.title }}</a>
                - {% if task.completed %}Completed{% else %}Pending{% endif %}
            </li>
        {% empty %}
            <li>No tasks available.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Sample content for add_task.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Add Task</title>
</head>
<body>
    <h1>Add a New Task</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Task</button>
    </form>
    <a href="{% url 'task_list' %}">Back to Task List</a>
</body>
</html>
"""

# Sample content for task_detail.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Task Detail</title>
</head>
<body>
    <h1>Task Detail</h1>
    <h2>{{ task.title }}</h2>
    <p>{{ task.description }}</p>
    <p>Status: {% if task.completed %}Completed{% else %}Pending{% endif %}</p>
    <a href="{% url 'task_list' %}">Back to Task List</a>
</body>
</html>
"""

# Step 11: Run the server to see your app in action

# python manage.py runserver
# Open your web browser and navigate to http://127.0.0.1:8000/tasks/ to view your to-do list app.
```